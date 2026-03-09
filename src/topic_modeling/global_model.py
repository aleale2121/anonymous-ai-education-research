import os

import pandas as pd
from .modeling_utils import build_topic_model


def run_global_model(
    input_path,
    embedding_model,
    vectorizer_model,
    representation_model,
    output_dir
):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_path)
    docs = df["clean_text"].tolist()

    topic_model = build_topic_model(
        embedding_model,
        vectorizer_model,
        representation_model,
        n_neighbors=15,
        n_components=5,
        min_dist=0.00,
        min_cluster_size=25,
        min_samples=10,
    )

    topics, _ = topic_model.fit_transform(docs)

    df["topic"] = topics

    topic_info = topic_model.get_topic_info()

    topic_info.to_csv(f"{output_dir}/topics.csv", index=False)
    df.to_csv(f"{output_dir}/data_with_topics.csv", index=False)

    topic_model.save(f"{output_dir}/model")

    return topic_model, df