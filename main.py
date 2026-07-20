from src.load_data import load_all_data
from src.clean_data import clean_data
from src.eda import run_eda
from src.ml import run_ml


def main():

    data = load_all_data()

    df = clean_data(data)

    run_eda(df)

    run_ml()

    print("\nProject executed successfully.")


if __name__ == "__main__":
    main()