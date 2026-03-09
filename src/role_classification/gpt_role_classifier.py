import itertools
import os
import re
import asyncio
import logging
import pandas as pd
from typing import List
from openai import AsyncOpenAI
from dotenv import load_dotenv

from src.data_collection.preprocess import clean_text

load_dotenv()
# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)
logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5"

# Fixed Roles
VALID_ROLES = {"educator", "student", "unknown"}

SYSTEM_PROMPT = """
You are an expert in analyzing the social roles of Reddit users in educational discussions.

Your task is to classify the author of the post into exactly ONE category:

educator = someone speaking from a position of teaching authority, instructional responsibility, or academic leadership
student  = someone speaking from a position of learning or academic participation
unknown  = cannot determine the role from the post 

RULES:
- Use only explicit context from the post.
- Do NOT hallucinate missing context.
- If unclear, choose "unknown".
- Output ONLY one of:
educator
student
unknown
(no punctuation, no extra text)
"""

# GPT Classification
async def classify_single_post(text: str, max_retries: int = 5):
    global students_count, educators_count
    backoff = 1.0
    user_prompt = (
        f"Post:\n{text}\n\n"
        "Return ONLY one word: educator, student, or unknown."
    )

    for attempt in range(1, max_retries + 1):
        try:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )

            raw = (response.choices[0].message.content or "").strip().lower()
            
            # Remove punctuation and extra whitespace
            response_role = re.sub(r"[^\w\s]", "", raw).strip()

            if response_role in VALID_ROLES:
                return response_role
        
            for role in VALID_ROLES:
                if re.search(rf"\b{role}\b", response_role):
                    return role
                
            logger.warning(f"[INVALID OUTPUT] attempt {attempt} — got '{raw}'")

        except Exception as e:
            logger.warning(f"[GPT ERROR] attempt {attempt} — {e}")

        if attempt == max_retries:
            return "unknown"

        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, 10.0)

    return "unknown"


async def classify_batch(texts: List[str]):
    tasks = [classify_single_post(t) for t in texts]
    return await asyncio.gather(*tasks)


# Data Preparation
def load_and_prepare(input_path: str):
    df = pd.read_csv(input_path)

    # clean only if not already cleaned
    if "clean_text" not in df.columns:
        logger.info("clean_text not found cleaning data")
        df["clean_text"] = df["body"].fillna("").apply(clean_text)

    df = df[df["clean_text"].str.len() > 20].copy()
    return df

# Main classification
async def run_role_classification(args):

    df = load_and_prepare(args.input)
    posts = df["clean_text"].tolist()
    all_results = []

    for i in range(0, len(posts), args.batch_size):
        batch_texts = posts[i:i + args.batch_size]
        logger.info(f"Processing batch {i} to {i + len(batch_texts)}")

        results = await classify_batch(batch_texts)
        all_results.extend(results)
         
        if educators_count>=1 and students_count>=1:
            break 

        await asyncio.sleep(0.5)

    
    remaining = len(df) - len(all_results)
    if remaining > 0:
        logger.info(f"Stopping early. Filling {remaining} rows with 'unknown'.")
        remaining_roles = list(itertools.islice(itertools.cycle(VALID_ROLES), remaining))
        all_results.extend(remaining_roles)
        
    df["role"] = all_results

    os.makedirs(args.output_dir, exist_ok=True)

    # Save full labeled dataset
    full_path = os.path.join(args.output_dir, "role_labeled_full.csv")
    df.to_csv(full_path, index=False)
    logger.info(f"Saved dataset => {full_path}")

    # Save split datasets in separate folders
    for role in VALID_ROLES:
        df_role = df[df["role"] == role]

        role_dir = os.path.join(args.output_dir, role)
        os.makedirs(role_dir, exist_ok=True)

        role_path = os.path.join(role_dir, f"reddit_{role}.csv")
        df_role.to_csv(role_path, index=False)

        logger.info(
            f"Saved {role} => {role_path} ({len(df_role)} rows)"
        )

    print(df["role"].value_counts())
