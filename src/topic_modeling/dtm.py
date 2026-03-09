import pandas as pd
from bertopic import BERTopic
import os

def run_dtm(model_path, input_path, output_dir, time_column="year"):

    # Load model
    topic_model = BERTopic.load(model_path)

    # Load dataset
    df = pd.read_csv(input_path)

    docs = df["clean_text"].tolist()
    topics = df["topic"].tolist()
    timestamps = df[time_column].tolist()

    # Compute dynamic topic modeling
    topics_over_time = topic_model.topics_over_time(
        docs=docs,
        timestamps=timestamps,
        topics=topics,
        nr_bins=8,
        global_tuning=True,
        evolution_tuning=True
    )

    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Save result
    save_path = os.path.join(output_dir, "topics_over_time.csv")
    topics_over_time.to_csv(save_path, index=False)

    print(f"Saved topics_over_time to {save_path}")

    return topics_over_time