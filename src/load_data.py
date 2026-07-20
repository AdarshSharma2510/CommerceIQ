from pathlib import Path

import pandas as pd

from src.config import (
    CUSTOMERS_FILE,
    ORDERS_FILE,
    ORDER_ITEMS_FILE,
    PAYMENTS_FILE,
    PRODUCTS_FILE,
    REVIEWS_FILE,
    SELLERS_FILE,
    TRANSLATION_FILE,
)


def _validate_file(file_path: Path) -> None:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{file_path}\n\n"
            "Please place the required CSV inside data/raw/"
        )


def load_all_data() -> dict[str, pd.DataFrame]:
    """
    Loads all raw datasets into a dictionary.
    """

    datasets = {
        "customers": CUSTOMERS_FILE,
        "orders": ORDERS_FILE,
        "order_items": ORDER_ITEMS_FILE,
        "payments": PAYMENTS_FILE,
        "products": PRODUCTS_FILE,
        "reviews": REVIEWS_FILE,
        "sellers": SELLERS_FILE,
        "translation": TRANSLATION_FILE,
    }

    loaded_data = {}

    print("\n========== LOADING DATA ==========\n")

    for name, path in datasets.items():

        _validate_file(path)

        df = pd.read_csv(path)

        loaded_data[name] = df

        print(f"✓ {name:<15} {df.shape}")

    print("\nAll datasets loaded successfully.\n")

    return loaded_data