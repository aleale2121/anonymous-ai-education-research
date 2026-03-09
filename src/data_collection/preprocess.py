import os
import re
import pandas as pd

def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^A-Za-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def load_and_clean(input_path):
    df = pd.read_csv(input_path)
    df["clean_text"] = df["body"].fillna("").apply(clean_text)
    df = df[df["clean_text"].str.len() > 20]
    return df


def load_keywords(ai_key_path=None):
    ai_keywords = []

    if ai_key_path and os.path.exists(ai_key_path):
        kws = (
            pd.read_csv(ai_key_path, header=None, names=["kw"])["kw"]
            .astype(str)
            .str.lower()
            .tolist()
        )
        ai_keywords.extend(kws)

    return sorted(set(ai_keywords))


def filter_ai(df, keywords):
    if not keywords:
        return df

    return df[df["clean_text"].apply(
        lambda t: any(k in t for k in keywords)
    )]


def preprocess_pipeline(
    input_path,
    output_path,
    ai_key_path=None,
    apply_ai_filter=False
):
    df = load_and_clean(input_path)

    if apply_ai_filter:
        keywords = load_keywords(ai_key_path)
        df = filter_ai(df, keywords)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Saved processed file → {output_path}")
    return df