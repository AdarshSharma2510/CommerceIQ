from src.load_data import load_all_data
from src.clean_data import clean_data


def main():

    data = load_all_data()

    df = clean_data(data)

    print(df.head())

    print(f"\nFinal Dataset Shape : {df.shape}")


if __name__ == "__main__":
    main()