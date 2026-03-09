import os
import argparse
import pandas as pd


def merge_files(input_dir: str, output_path: str):

    if not os.path.exists(input_dir):
        raise ValueError(f"Input directory does not exist: {input_dir}")

    files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".csv")
    ]

    if not files:
        print("No CSV files found.")
        return

    print(f"Found {len(files)} CSV files.")

    dfs = []

    for file in sorted(files):
        print(f"Reading {file}")
        dfs.append(pd.read_csv(file))

    merged = pd.concat(dfs, ignore_index=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    merged.to_csv(output_path, index=False)

    print(f"\nSaved merged dataset → {output_path}")
    print(f"Total rows: {len(merged)}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_dir",
        default="data/raw",
        help="Directory containing CSV files to merge"
    )

    parser.add_argument(
        "--output",
        default="data/processed/reddit_ai_global.csv",
        help="Output merged CSV file"
    )

    args = parser.parse_args()

    merge_files(
        input_dir=args.input_dir,
        output_path=args.output
    )


if __name__ == "__main__":
    main()