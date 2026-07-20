import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import CLEAN_DATA_FILE, EDA_IMAGE_DIR
from src.utils import save_plot, set_plot_style, print_heading


set_plot_style()


def overview_analysis(df: pd.DataFrame) -> None:
    """
    Prints high-level business KPIs.
    """

    print_heading("Executive Summary")

    revenue = df["total_order_value"].sum()
    orders = df["order_id"].nunique()
    customers = df["customer_unique_id"].nunique()
    avg_order = df["total_order_value"].mean()
    avg_review = df["review_score"].mean()

    print(f"Total Revenue        : ${revenue:,.2f}")
    print(f"Total Orders         : {orders:,}")
    print(f"Unique Customers     : {customers:,}")
    print(f"Average Order Value  : ${avg_order:.2f}")
    print(f"Average Review Score : {avg_review:.2f}")


def sales_analysis(df: pd.DataFrame):

    print_heading("Sales Analysis")

    monthly_sales = (
        df.groupby("purchase_month")["total_order_value"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=monthly_sales,
        x="purchase_month",
        y="total_order_value",
        marker="o",
        linewidth=2.5,
    )

    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")

    save_plot(
        EDA_IMAGE_DIR,
        "monthly_revenue.png"
    )

    print(
        "Highest Revenue Month:",
        monthly_sales.loc[
            monthly_sales["total_order_value"].idxmax(),
            "purchase_month",
        ],
    )

    monthly_orders = (
        df.groupby("purchase_month")["order_id"]
        .count()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=monthly_orders,
        x="purchase_month",
        y="order_id",
    )

    plt.title("Orders by Month")

    save_plot(
        EDA_IMAGE_DIR,
        "monthly_orders.png"
    )

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["total_order_value"],
        bins=40,
        kde=True,
    )

    plt.title("Distribution of Order Value")

    save_plot(
        EDA_IMAGE_DIR,
        "order_value_distribution.png"
    )


def customer_analysis(df: pd.DataFrame):

    print_heading("Customer Analysis")

    plt.figure(figsize=(8, 6))

    sns.countplot(
        data=df,
        x="payment_type",
        order=df["payment_type"].value_counts().index,
    )

    plt.xticks(rotation=30)

    plt.title("Payment Methods")

    save_plot(
        EDA_IMAGE_DIR,
        "payment_methods.png"
    )

    plt.figure(figsize=(8, 6))

    sns.countplot(
        data=df,
        x="review_score",
    )

    plt.title("Review Score Distribution")

    save_plot(
        EDA_IMAGE_DIR,
        "review_scores.png"
    )

    hourly_orders = (
        df.groupby("purchase_hour")
        .size()
        .reset_index(name="orders")
    )

    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=hourly_orders,
        x="purchase_hour",
        y="orders",
        marker="o",
    )

    plt.title("Orders by Hour")

    save_plot(
        EDA_IMAGE_DIR,
        "orders_by_hour.png"
    )

    weekday_orders = (
        df.groupby("purchase_weekday")
        .size()
        .reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
        .reset_index(name="orders")
    )

    plt.figure(figsize=(11, 6))

    sns.barplot(
        data=weekday_orders,
        x="purchase_weekday",
        y="orders",
    )

    plt.xticks(rotation=20)

    plt.title("Orders by Weekday")

    save_plot(
        EDA_IMAGE_DIR,
        "orders_by_weekday.png"
    )
def product_analysis(df: pd.DataFrame) -> None:

    print_heading("Product Analysis")

    top_categories = (
        df.groupby("main_category")["order_id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=top_categories,
        x="order_id",
        y="main_category",
    )

    plt.title("Top 10 Product Categories by Orders")
    plt.xlabel("Orders")
    plt.ylabel("Category")

    save_plot(
        EDA_IMAGE_DIR,
        "top_categories.png",
    )

    category_revenue = (
        df.groupby("main_category")["total_order_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=category_revenue,
        x="total_order_value",
        y="main_category",
    )

    plt.title("Top 10 Categories by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Category")

    save_plot(
        EDA_IMAGE_DIR,
        "category_revenue.png",
    )


def logistics_analysis(df: pd.DataFrame) -> None:

    print_heading("Logistics Analysis")

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["delivery_days"],
        bins=30,
        kde=True,
    )

    plt.title("Delivery Time Distribution")

    save_plot(
        EDA_IMAGE_DIR,
        "delivery_days.png",
    )

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["delivery_delay"],
        bins=30,
        kde=True,
    )

    plt.title("Delivery Delay Distribution")

    save_plot(
        EDA_IMAGE_DIR,
        "delivery_delay.png",
    )

    plt.figure(figsize=(7, 5))

    sns.countplot(
        data=df,
        x="is_delayed",
    )

    plt.title("Delayed vs On-Time Orders")

    save_plot(
        EDA_IMAGE_DIR,
        "delayed_orders.png",
    )


def correlation_analysis(df: pd.DataFrame) -> None:

    print_heading("Correlation Analysis")

    numeric_df = df.select_dtypes(include="number")

    plt.figure(figsize=(12, 10))

    sns.heatmap(
        numeric_df.corr(),
        cmap="coolwarm",
        annot=False,
        square=True,
    )

    plt.title("Correlation Heatmap")

    save_plot(
        EDA_IMAGE_DIR,
        "correlation_heatmap.png",
    )


def geographical_analysis(df: pd.DataFrame) -> None:

    print_heading("Geographical Analysis")

    if "customer_state" not in df.columns:
        print("customer_state column not found. Skipping geographical analysis.")
        return

    top_states = (
        df.groupby("customer_state")["total_order_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=top_states,
        x="customer_state",
        y="total_order_value",
    )

    plt.title("Top States by Revenue")
    plt.xlabel("State")
    plt.ylabel("Revenue")

    save_plot(
        EDA_IMAGE_DIR,
        "top_states.png",
    )


def order_status_analysis(df: pd.DataFrame) -> None:

    print_heading("Order Status")

    plt.figure(figsize=(10, 6))

    sns.countplot(
        data=df,
        y="order_status",
        order=df["order_status"].value_counts().index,
    )

    plt.title("Order Status Distribution")

    save_plot(
        EDA_IMAGE_DIR,
        "order_status.png",
    )


def run_eda(df: pd.DataFrame) -> None:

    overview_analysis(df)

    sales_analysis(df)

    customer_analysis(df)

    product_analysis(df)

    logistics_analysis(df)

    order_status_analysis(df)

    geographical_analysis(df)

    correlation_analysis(df)

    print("\nEDA completed successfully.")
    print(f"Visualizations saved to:\n{EDA_IMAGE_DIR}")


if __name__ == "__main__":

    dataframe = pd.read_csv(CLEAN_DATA_FILE)

    run_eda(dataframe)