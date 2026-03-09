import os
import time
import logging
import pandas as pd
from tqdm import tqdm
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

MODEL = "gpt-5"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an expert in semantic topic interpretation.

Given representative documents and topic keywords,
produce:

Topic:
<short label>

Topic Summary:
<concise summary under 30 words>

Output EXACTLY in this format.
"""


# GPT CALL 
def gpt_interpret_topic(rep_docs: str, key_words: str, retries: int = 5):

    user_prompt = f"""
Representative docs:
{rep_docs}

Keyword:
{key_words}
"""

    backoff = 1.0

    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )

            text = (response.choices[0].message.content or "").strip()

            if text:
                return text

        except Exception as e:
            logger.warning(f"GPT error attempt {attempt}: {e}")

        time.sleep(backoff)
        backoff = min(backoff * 2, 10)

    return "Topic:\nUnknown\nTopic Summary:\nUnknown"


# PARSER-
def parse_interpretation(text: str):

    topic_label = ""
    topic_summary = ""

    if "Topic Summary:" in text:
        parts = text.split("Topic Summary:")
        topic_label = parts[0].replace("Topic:", "").strip()
        topic_summary = parts[1].strip()

    return topic_label, topic_summary


# MAIN REFINEMENT FUNCTION
def refine_topics(
    input_path: str,
    output_path: str,
    corpus_name: Optional[str] = None
):

    df = pd.read_csv(input_path)
    total_count = df["Count"].sum()

    topic_labels = []
    topic_summaries = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Refining topics"):

        interpretation = gpt_interpret_topic(
            rep_docs=str(row.get("Representative_Docs", "")),
            key_words=str(row.get("Representation", ""))
        )

        label, summary = parse_interpretation(interpretation)

        topic_labels.append(label)
        topic_summaries.append(summary)

    df["Topic summary"] = topic_labels
    df["Topic description"] = topic_summaries

    percent_column = "% of corpus"
    if corpus_name:
        percent_column = f"% of {corpus_name} corpus"

    df[percent_column] = (df["Count"] / total_count * 100).round(3)

    final = df[
        ["Topic", "Topic summary", "Topic description", "Count", percent_column]
    ]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.to_csv(output_path, index=False)

    print(f"Saved refined topics → {output_path}")

    return final