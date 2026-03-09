import os
import pandas as pd
from tqdm import tqdm
from .modeling_utils import build_topic_model


def run_yearly_models(
    input_path,
    embedding_model,
    vectorizer_model,
    representation_model,
    output_dir
):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_path)
    years = sorted(df["year"].unique())

    for year in tqdm(years):
        df_year = df[df["year"] == year].copy()

        if len(df_year) < 200:
            print(f"Skipping {year}, too few docs.")
            continue

        docs = df_year["clean_text"].tolist()

        topic_model = build_topic_model(
            embedding_model,
            vectorizer_model,
            representation_model,
            n_neighbors=15,
            n_components=5,
            min_dist=0.00,
            min_cluster_size=20,
            min_samples=10
        )

        topics, probs = topic_model.fit_transform(docs)
        df_year["topic"] = topics

        year_dir = f"{output_dir}/{year}"
        os.makedirs(year_dir, exist_ok=True)

        df_year.to_csv(f"{year_dir}/data_with_topics.csv", index=False)
        topic_model.get_topic_info().to_csv(
            f"{year_dir}/topics.csv", index=False
        )
        topic_model.save(f"{year_dir}/model")

        print(f"Finished {year}")