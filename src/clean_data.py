import numpy as np
import pandas as pd

from src.config import CLEAN_DATA_FILE


def clean_data(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Cleans and prepares the Olist dataset.
    Returns one row per order.
    """

    print("\n========== CLEANING DATA ==========\n")

    customers = data["customers"].copy()
    orders = data["orders"].copy()
    order_items = data["order_items"].copy()
    payments = data["payments"].copy()
    products = data["products"].copy()
    reviews = data["reviews"].copy()
    translation = data["translation"].copy()

    # ---------------------------------------------------------
    # Convert datetime columns
    # ---------------------------------------------------------

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for col in date_columns:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    print("✓ Converted datetime columns")

    # ---------------------------------------------------------
    # Translate product category names
    # ---------------------------------------------------------

    products = products.merge(
        translation,
        on="product_category_name",
        how="left"
    )

    products["product_category_name_english"] = (
        products["product_category_name_english"]
        .fillna("Unknown")
    )

    # ---------------------------------------------------------
    # Merge products into order items
    # ---------------------------------------------------------

    order_items = order_items.merge(
        products[
            [
                "product_id",
                "product_category_name_english",
            ]
        ],
        on="product_id",
        how="left"
    )

    # ---------------------------------------------------------
    # Aggregate Order Items
    # ---------------------------------------------------------

    order_items_agg = (
        order_items
        .groupby("order_id")
        .agg(
            total_items=("order_item_id", "count"),
            total_product_price=("price", "sum"),
            total_freight=("freight_value", "sum"),
            avg_item_price=("price", "mean"),
            unique_products=("product_id", "nunique"),
            main_category=(
                "product_category_name_english",
                lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown"
            )
        )
        .reset_index()
    )

    print("✓ Aggregated order items")

    # ---------------------------------------------------------
    # Aggregate Payments
    # ---------------------------------------------------------

    payments_agg = (
        payments
        .groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_installments=("payment_installments", "max"),
            payment_type=(
                "payment_type",
                lambda x: x.mode().iloc[0]
            )
        )
        .reset_index()
    )

    print("✓ Aggregated payments")

    # ---------------------------------------------------------
    # Aggregate Reviews
    # ---------------------------------------------------------

    reviews_agg = (
        reviews
        .groupby("order_id")
        .agg(
            review_score=("review_score", "mean")
        )
        .reset_index()
    )

    print("✓ Aggregated reviews")

    # ---------------------------------------------------------
    # Merge Everything
    # ---------------------------------------------------------

    df = (
        orders
        .merge(customers, on="customer_id", how="left")
        .merge(order_items_agg, on="order_id", how="left")
        .merge(payments_agg, on="order_id", how="left")
        .merge(reviews_agg, on="order_id", how="left")
    )

    print(f"✓ Final merged shape : {df.shape}")

    # ---------------------------------------------------------
    # Missing Values
    # ---------------------------------------------------------

    numeric_columns = df.select_dtypes(include=np.number).columns

    categorical_columns = df.select_dtypes(include="object").columns

    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())

    for col in categorical_columns:
        df[col] = df[col].fillna("Unknown")

    # ---------------------------------------------------------
    # Feature Engineering
    # ---------------------------------------------------------

    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.days

    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"]
        - df["order_purchase_timestamp"]
    ).dt.days

    df["delivery_delay"] = (
        df["delivery_days"]
        - df["estimated_delivery_days"]
    )

    df["delivery_delay"] = df["delivery_delay"].fillna(0)

    df["is_delayed"] = (
        df["delivery_delay"] > 0
    ).astype(int)

    df["purchase_year"] = (
        df["order_purchase_timestamp"].dt.year
    )

    df["purchase_month"] = (
        df["order_purchase_timestamp"].dt.month
    )

    df["purchase_day"] = (
        df["order_purchase_timestamp"].dt.day
    )

    df["purchase_hour"] = (
        df["order_purchase_timestamp"].dt.hour
    )

    df["purchase_weekday"] = (
        df["order_purchase_timestamp"].dt.day_name()
    )

    df["purchase_quarter"] = (
        df["order_purchase_timestamp"].dt.quarter
    )

    df["total_order_value"] = (
        df["total_product_price"]
        + df["total_freight"]
    )

    # ---------------------------------------------------------
    # Remove duplicates
    # ---------------------------------------------------------

    before = len(df)

    df.drop_duplicates(
        subset="order_id",
        inplace=True
    )

    after = len(df)

    print(f"✓ Removed {before-after} duplicate rows")

    # ---------------------------------------------------------
    # Reorder Important Columns
    # ---------------------------------------------------------

    first_columns = [
        "order_id",
        "customer_id",
        "customer_unique_id",
        "order_status",
        "purchase_year",
        "purchase_month",
        "purchase_day",
        "purchase_hour",
        "purchase_weekday",
        "purchase_quarter",
        "total_items",
        "unique_products",
        "main_category",
        "total_product_price",
        "total_freight",
        "total_order_value",
        "payment_value",
        "payment_installments",
        "payment_type",
        "review_score",
        "delivery_days",
        "estimated_delivery_days",
        "delivery_delay",
        "is_delayed",
    ]

    remaining_columns = [
        col
        for col in df.columns
        if col not in first_columns
    ]

    df = df[first_columns + remaining_columns]

    # ---------------------------------------------------------
    # Save Dataset
    # ---------------------------------------------------------

    df.to_csv(
        CLEAN_DATA_FILE,
        index=False
    )

    print(f"✓ Saved cleaned dataset to\n{CLEAN_DATA_FILE}")

    print("\n========== CLEANING COMPLETE ==========\n")

    return df