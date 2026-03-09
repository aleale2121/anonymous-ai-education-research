import argparse
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from bertopic.representation import KeyBERTInspired

from src.topic_modeling.global_model import run_global_model
from src.topic_modeling.yearly_model import run_yearly_models
from src.topic_modeling.role_model import run_role_model

def initialize_models():
    embedding_model = SentenceTransformer("BAAI/bge-large-en-v1.5")

    vectorizer_model = CountVectorizer(
        stop_words=list(text.ENGLISH_STOP_WORDS),
        ngram_range=(1, 2),
        min_df=3
    )

    representation_model = KeyBERTInspired()

    return embedding_model, vectorizer_model, representation_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--mode", required=True, choices=["global", "yearly", "role"])
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    embedding_model, vectorizer_model, representation_model = initialize_models()

    if args.mode == "global":
        run_global_model(
            args.input,
            embedding_model,
            vectorizer_model,
            representation_model,
            args.output
        )

    elif args.mode == "yearly":
        run_yearly_models(
            args.input,
            embedding_model,
            vectorizer_model,
            representation_model,
            args.output
        )
    
    elif args.mode == "role":
        run_role_model(
            args.input,
            embedding_model,
            vectorizer_model,
            representation_model,
            args.output
        )


if __name__ == "__main__":
    main()