from src.load_data import load_all_data
from src.clean_data import clean_data
from src.eda import run_eda


def main():

    data = load_all_data()

    df = clean_data(data)

    run_eda(df)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()