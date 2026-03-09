import argparse
import asyncio
import pandas as pd
from src.thematic_categorization.classifier import classify_dataframe


async def run(args):

    df = pd.read_csv(args.input)

    df = await classify_dataframe(df)

    df.to_csv(args.output, index=False)

    print(f"Saved → {args.output}")

    grouped = (
        df.groupby(["Topic Category", "year"])
        .size()
        .reset_index(name="count")
    )

    pivot = grouped.pivot(
        index="Topic Category",
        columns="year",
        values="count"
    ).fillna(0).astype(int)

    pivot = pivot[sorted(pivot.columns)]

    # Add TOTAL row
    pivot.loc["TOTAL"] = pivot.sum(axis=0)

    counts_output = args.output.replace(".csv", "_yearly_counts.csv")

    pivot.to_csv(counts_output)

    print(f"Saved category counts → {counts_output}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    asyncio.run(run(args))


if __name__ == "__main__":
    main()