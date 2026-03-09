import argparse
from src.data_collection.preprocess import preprocess_pipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw CSV")
    parser.add_argument("--output", required=True, help="Path to cleaned CSV")
    parser.add_argument("--ai_filter", action="store_true", help="Apply AI filtering")
    parser.add_argument("--ai_keywords", default=None)

    args = parser.parse_args()

    preprocess_pipeline(
        input_path=args.input,
        output_path=args.output,
        ai_key_path=args.ai_keywords,
        apply_ai_filter=args.ai_filter
    )

if __name__ == "__main__":
    main()