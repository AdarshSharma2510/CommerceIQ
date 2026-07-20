from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from src.config import (
    CLEAN_DATA_FILE,
    CUSTOMER_SEGMENTS_FILE,
    MODEL_FILE,
)
from src.utils import save_plot, print_heading, set_plot_style

set_plot_style()

ML_IMAGE_DIR = Path("images") / "ml"
ML_IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    """
    Load cleaned dataset.
    """

    print_heading("Loading Dataset")

    df = pd.read_csv(
        CLEAN_DATA_FILE,
        parse_dates=["order_purchase_timestamp"],
    )

    print(df.shape)

    return df


def create_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Recency, Frequency and Monetary features.
    """

    print_heading("Creating RFM Table")

    reference_date = (
        df["order_purchase_timestamp"].max()
        + pd.Timedelta(days=1)
    )

    rfm = (
        df.groupby("customer_unique_id")
        .agg(
            Recency=(
                "order_purchase_timestamp",
                lambda x: (reference_date - x.max()).days,
            ),
            Frequency=("order_id", "count"),
            Monetary=("total_order_value", "sum"),
        )
        .reset_index()
    )

    print(rfm.head())

    return rfm


def perform_customer_segmentation(
    df: pd.DataFrame,
) -> pd.DataFrame:

    print_heading("Customer Segmentation")

    rfm = create_rfm(df)

    scaler = StandardScaler()

    features = scaler.fit_transform(
        rfm[
            [
                "Recency",
                "Frequency",
                "Monetary",
            ]
        ]
    )

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10,
    )

    rfm["Cluster"] = kmeans.fit_predict(
        features
    )

    cluster_summary = (
        rfm.groupby("Cluster")
        .agg(
            Customers=("Cluster", "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean"),
        )
        .round(2)
    )

    print("\nCluster Summary\n")
    print(cluster_summary)

    pca = PCA(
        n_components=2,
        random_state=42,
    )

    reduced = pca.fit_transform(
        features
    )

    plot_df = pd.DataFrame(
        {
            "PC1": reduced[:, 0],
            "PC2": reduced[:, 1],
            "Cluster": rfm["Cluster"],
        }
    )

    plt.figure(figsize=(10, 7))

    sns.scatterplot(
        data=plot_df,
        x="PC1",
        y="PC2",
        hue="Cluster",
        palette="Set2",
        s=60,
    )

    plt.title("Customer Segmentation using KMeans")

    save_plot(
        ML_IMAGE_DIR,
        "customer_segments.png",
    )

    rfm.to_csv(
        CUSTOMER_SEGMENTS_FILE,
        index=False,
    )

    print(
        "\nCustomer Segments Saved Successfully."
    )

    return rfm


def prepare_ml_data(df: pd.DataFrame):
    """
    Prepare the dataset for delivery delay prediction.
    """

    print_heading("Preparing ML Dataset")

    ml_df = df.copy()

    drop_columns = [
        "order_id",
        "customer_id",
        "customer_unique_id",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "delivery_delay",
    ]

    existing_columns = [
        col
        for col in drop_columns
        if col in ml_df.columns
    ]

    ml_df.drop(columns=existing_columns, inplace=True)

    categorical_columns = ml_df.select_dtypes(
        include="object"
    ).columns

    encoders = {}

    for column in categorical_columns:

        encoder = LabelEncoder()

        ml_df[column] = encoder.fit_transform(
            ml_df[column].astype(str)
        )

        encoders[column] = encoder

    X = ml_df.drop(columns="is_delayed")

    y = ml_df["is_delayed"]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )


def train_random_forest(X_train, y_train):
    """
    Train the Random Forest classifier.
    """

    print_heading("Training Random Forest")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(
    model,
    X_test,
    y_test,
    feature_names,
):
    """
    Evaluate model performance and save visualizations.
    """

    print_heading("Model Evaluation")

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    auc = roc_auc_score(
        y_test,
        probabilities,
    )

    print(f"Accuracy : {accuracy:.4f}")
    print(f"ROC AUC  : {auc:.4f}")

    print("\nClassification Report\n")

    print(
        classification_report(
            y_test,
            predictions,
        )
    )

    cm = confusion_matrix(
        y_test,
        predictions,
    )

    plt.figure(figsize=(7, 6))

    ConfusionMatrixDisplay(
        confusion_matrix=cm
    ).plot(cmap="Blues")

    plt.title("Confusion Matrix")

    save_plot(
        ML_IMAGE_DIR,
        "confusion_matrix.png",
    )

    RocCurveDisplay.from_estimator(
        model,
        X_test,
        y_test,
    )

    plt.title("ROC Curve")

    save_plot(
        ML_IMAGE_DIR,
        "roc_curve.png",
    )

    importance = (
        pd.Series(
            model.feature_importances_,
            index=feature_names,
        )
        .sort_values(ascending=False)
        .head(15)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=importance.values,
        y=importance.index,
    )

    plt.title("Top 15 Feature Importances")

    save_plot(
        ML_IMAGE_DIR,
        "feature_importance.png",
    )


def save_model(model):
    """
    Save trained model.
    """

    joblib.dump(
        model,
        MODEL_FILE,
    )

    print(f"\nModel saved to:\n{MODEL_FILE}")


def run_ml():
    """
    Execute complete ML pipeline.
    """

    df = load_dataset()

    perform_customer_segmentation(df)

    X_train, X_test, y_train, y_test = (
        prepare_ml_data(df)
    )

    model = train_random_forest(
        X_train,
        y_train,
    )

    evaluate_model(
        model,
        X_test,
        y_test,
        X_train.columns,
    )

    save_model(model)

    print_heading("ML Pipeline Complete")


if __name__ == "__main__":

    run_ml()