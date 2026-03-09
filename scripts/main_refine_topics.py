import argparse
from src.topic_refinement.refiner import refine_topics


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--corpus_name", default=None)

    args = parser.parse_args()
   
    refine_topics(
        input_path=args.input,
        output_path=args.output,
        corpus_name=args.corpus_name
    ) 

if __name__ == "__main__":
    main()