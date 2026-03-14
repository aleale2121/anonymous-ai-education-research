import argparse

from src.thematic_categorization.classifier import categorize_topics


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()
    categorize_topics(args.input,args.output)


if __name__ == "__main__":
    main()