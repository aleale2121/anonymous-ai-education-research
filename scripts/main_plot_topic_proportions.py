import argparse
from src.visualization.topic_proportion_plot import plot_topic_proportions


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    plot_topic_proportions(
        input_path=args.input,
        output_path=args.output
    )


if __name__ == "__main__":
    main()