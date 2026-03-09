import json
import os
from tqdm import tqdm
from openai import AsyncOpenAI
from rapidfuzz import process
from dotenv import load_dotenv

from .categories import CATEGORIES

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5"

def normalize_category(label):
    match, score, _ = process.extractOne(label, CATEGORIES)

    if score > 70:
        return match

    return "Other Off-Topic / General Discussions"

async def classify_batch(batch_texts):

    joined = ""
    for i, text in enumerate(batch_texts):
        joined += f"ITEM {i}:\n{text}\n\n"

    prompt = f"""
You are a context-aware classifier for Reddit posts about AI and Education.

Assign EACH item to EXACTLY ONE category from this list:

{CATEGORIES}

Return JSON ONLY in this format:
{{ "labels": ["Category for ITEM 0", "Category for ITEM 1"] }}

Items:
{joined}
"""

    response = await client.responses.create(
        model=MODEL,
        input=prompt
    )

    try:
        raw = response.output_text
        data = json.loads(raw)

        labels = data["labels"]
        if len(labels) != len(batch_texts):
            raise ValueError("Invalid label count")

        labels = [normalize_category(l) for l in labels]
        return labels
    
    except Exception as e:
        return ["Other Off-Topic / General Discussions"] * len(batch_texts)


async def classify_dataframe(df, text_column="clean_text", batch_size=20):

    results = []
    count = 0
    for start in tqdm(range(0, len(df), batch_size)):

        batch = df.iloc[start:start+batch_size][text_column].astype(str).tolist()
        labels = await classify_batch(batch)
        results.extend(labels)
        count +=1
        if (count == 5):
            break
    remaining = len(df)-len(results)
    if remaining > 0:
        results += ["Other Off-Topic / General Discussions"] * (remaining)

    df["Topic Category"] = results

    return df