import os
import json
import logging
import pandas as pd
from tqdm import tqdm
from typing import Optional
from openai import OpenAI
from rapidfuzz import process
from dotenv import load_dotenv

from .categories import CATEGORIES

load_dotenv()
logger = logging.getLogger(__name__)

MODEL = "gpt-5"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_category(label):
    match, score, _ = process.extractOne(label, CATEGORIES)

    if score > 70:
        return match

    return "Other Off-Topic / General Discussions"


SYSTEM_PROMPT = f"""
You are an expert in AI-in-education discourse analysis.

Your task is to assign a discovered topic to EXACTLY ONE category.

Available categories:
{CATEGORIES}

Return JSON only in this format:

{{ "category": "Chosen Category" }}
"""


def gpt_classify_topic(rep_docs: str, keywords: str):

    prompt = f"""
Topic Keywords:
{keywords}

Representative Posts:
{rep_docs}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    try:
        raw = response.choices[0].message.content
        data = json.loads(raw)

        label = data["category"]
        label = normalize_category(label)

        return label

    except Exception as e:
        logger.warning(f"Classification error: {e}")
        return "Other Off-Topic / General Discussions"


def categorize_topics(
    input_path: str,
    output_path: str
):

    df = pd.read_csv(input_path)

    categories = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Categorizing topics"):

        category = gpt_classify_topic(
            rep_docs=str(row.get("Representative_Docs", "")),
            keywords=str(row.get("Representation", ""))
        )

        categories.append(category)

    df["Topic Category"] = categories

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Saved categorized topics → {output_path}")

    return df