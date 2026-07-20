from pathlib import Path

# ======================================================
# PROJECT ROOT
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ======================================================
# DATA DIRECTORIES
# ======================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# ======================================================
# OTHER DIRECTORIES
# ======================================================

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SQL_DIR = PROJECT_ROOT / "sql"
MODELS_DIR = PROJECT_ROOT / "models"
IMAGES_DIR = PROJECT_ROOT / "images"
REPORTS_DIR = PROJECT_ROOT / "reports"

# ======================================================
# RAW DATA FILES
# ======================================================

CUSTOMERS_FILE = RAW_DATA_DIR / "olist_customers_dataset.csv"
ORDERS_FILE = RAW_DATA_DIR / "olist_orders_dataset.csv"
ORDER_ITEMS_FILE = RAW_DATA_DIR / "olist_order_items_dataset.csv"
PAYMENTS_FILE = RAW_DATA_DIR / "olist_order_payments_dataset.csv"
PRODUCTS_FILE = RAW_DATA_DIR / "olist_products_dataset.csv"
REVIEWS_FILE = RAW_DATA_DIR / "olist_order_reviews_dataset.csv"
SELLERS_FILE = RAW_DATA_DIR / "olist_sellers_dataset.csv"
TRANSLATION_FILE = RAW_DATA_DIR / "product_category_name_translation.csv"

# ======================================================
# PROCESSED DATA
# ======================================================

CLEAN_DATA_FILE = PROCESSED_DATA_DIR / "ecommerce_cleaned.csv"

# ======================================================
# RANDOM STATE
# ======================================================

RANDOM_STATE = 42


# ======================================================
# OUTPUT FILES
# ======================================================

CUSTOMER_SEGMENTS_FILE = PROCESSED_DATA_DIR / "customer_segments.csv"

MODEL_FILE = MODELS_DIR / "delivery_delay_model.pkl"

# ======================================================
# IMAGE OUTPUT
# ======================================================

EDA_IMAGE_DIR = IMAGES_DIR / "eda"

EDA_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

MODELS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


ML_IMAGE_DIR = IMAGES_DIR / "ml"

ML_IMAGE_DIR.mkdir(parents=True, exist_ok=True)