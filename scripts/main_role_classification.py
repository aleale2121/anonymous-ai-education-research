# CLI Entry
import argparse
import asyncio

from src.role_classification.gpt_role_classifier import run_role_classification


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--batch_size", type=int, default=50)

    args = parser.parse_args()

    asyncio.run(run_role_classification(args))


if __name__ == "__main__":
    main()