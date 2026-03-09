import argparse
from src.topic_modeling.dtm import run_dtm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--time_column", default="year")

    args = parser.parse_args()

    run_dtm(
        model_path=args.model,
        input_path=args.input,
        output_dir=args.output,
        time_column=args.time_column
    )

if __name__ == "__main__":
    main()