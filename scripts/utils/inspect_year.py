import argparse
import pandas as pd


def inspect_year(input_path, date_col):

    df = pd.read_csv(input_path)

    # df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # print(sorted(df[date_col].dt.year.unique()))
    df["date"] = pd.to_datetime(df[date_col], unit="s")    
    unique_dates = (
        df["date"]
        .dt.date
        .drop_duplicates()
        .sort_values()
    )

    print(unique_dates)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--date_col", required=True)

    args = parser.parse_args()
    inspect_year(args.input,args.date_col)


if __name__ == "__main__":
    main()