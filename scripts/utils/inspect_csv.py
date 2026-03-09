import argparse
import pandas as pd


def inspect_csv(input_path):

    df = pd.read_csv(input_path)

    print("\nDataset Info")
    print("------------")

    print(f"File: {input_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn Names:")
    for col in df.columns:
        print(f" - {col}")

    print("\nFirst 5 Rows:")
    print(df.head())


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Input CSV file"
    )
  
    args = parser.parse_args()
    inspect_csv(args.input)


if __name__ == "__main__":
    main()