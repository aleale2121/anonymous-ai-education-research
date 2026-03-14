import argparse
import pandas as pd


def inspect_unique(input_path, col):

    df = pd.read_csv(input_path)

    if col not in df.columns:
        print(f"Column '{col}' not found.")
        return

    unique_values = sorted(df[col].dropna().unique())

    for val in unique_values:
        print(val)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--col", required=True)

    args = parser.parse_args()

    inspect_unique(args.input, args.col)


if __name__ == "__main__":
    main()