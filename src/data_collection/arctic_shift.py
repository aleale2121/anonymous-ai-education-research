import csv
import os
import re
from datetime import datetime
import requests

#  Arctic Shift API base URL
BASE_URL = "https://arctic-shift.photon-reddit.com/api"

# Target subreddits
SUBREDDITS = [
    "Teachers", "Education", "Students", "GradSchool", "OnlineLearning",
    "AskAcademia", "college", "professors", "edtech", "HigherEducation",
    "homeschool", "Teaching", "learnprogramming", "study", "academia",
    "cscareerquestions", "applyingtocollege", "careerguidance",
    "datascience", 
    "MachineLearning", "ArtificialIntelligence",
    "computervision", "deeplearning", "OpenAI"
]

# AI keyword pattern
AI_PATTERN = re.compile(
    r"\b("
    r"ai|artificial intelligence|machine learning|deep learning|neural network|"
    r"gpt|llm|chatgpt|openai|bert|transformer|"
    r"nlp|natural language processing|data science|computer vision|"
    r"reinforcement learning|generative model|diffusion model|"
    r"stable diffusion|prompt engineering|autonomous agent|rag|"
    r"fine[- ]?tuning|zero[- ]?shot|few[- ]?shot|"
    r"large language model|ai model|ai tool|ai system|ai ethics"
    r")\b",
    re.IGNORECASE
)


def is_ai_related(text):
    """Check if text mentions AI-related keywords."""
    return bool(AI_PATTERN.search(text or ""))


def save_row(item_id, item_type, body, created_utc, subreddit, year, month, link):
    """Save to a per-year CSV file (auto-creates + writes header once)."""
    DATA_DIR = os.path.join("data", "raw")
    os.makedirs(DATA_DIR, exist_ok=True)

    filename = os.path.join(DATA_DIR, f"reddit_ai_{year}.csv")
    write_header = not os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["id", "type", "created_utc", "body",
                             "link", "subreddit", "year", "month"])

        writer.writerow([
            item_id, item_type, created_utc,
            (body or "").replace("\n", " ").replace("\r", " ").strip(),
            link, subreddit, year, month
        ])

def month_ranges(start_year=2018, start_month=1, end_year=2025, end_month=12):
    """Yield (start_date, end_date, year, month) inclusive."""
    current = datetime(start_year, start_month, 1)
    end = datetime(end_year, end_month, 1)
    while current <= end:
        next_month = datetime(
            current.year + (current.month // 12),
            (current.month % 12) + 1,
            1
        )
        yield current.strftime("%Y-%m-%d"), next_month.strftime("%Y-%m-%d"), current.year, current.month
        current = next_month


def fetch_data(subreddit, after, before, kind="posts"):
    """Fetch posts or comments from Arctic Shift API."""
    url = f"{BASE_URL}/{kind}/search"
    params = {
        "subreddit": subreddit.lower(),
        "after": after,
        "before": before,
        "limit": "auto",
        "sort": "asc"
    }
    try:
        r = requests.get(url, params=params, timeout=90)
        r.raise_for_status()
        return r.json().get("data", [])
    except Exception as e:
        print(f"Error fetching {kind} from r/{subreddit} ({after}-{before}): {e}")
        return []


def fetch_comment_tree(post_id):
    """Fetch full comment tree for a given post ID and flatten it."""
    url = f"{BASE_URL}/comments/tree"
    params = {
        "link_id": f"t3_{post_id}",
        "limit": 9999,
    }
    try:
        r = requests.get(url, params=params, timeout=90)
        r.raise_for_status()
        data = r.json().get("data", [])
        flat = flatten_comment_tree(data)
        return flat
    except Exception as e:
        print(f"Error fetching comment tree for post {post_id}: {e}")
        return []


def flatten_comment_tree(tree):
    """Flatten nested Reddit comment tree to a flat list of comment dicts."""
    flat = []

    def _flatten(nodes):
        for node in nodes:
            if node.get("kind") != "t1":
                continue
            data = node.get("data", {})
            flat.append({
                "id": data.get("id"),
                "author": data.get("author"),
                "body": data.get("body"),
                "created_utc": data.get("created_utc"),
                "score": data.get("score"),
                "parent_id": data.get("parent_id"),
                "link_id": data.get("link_id"),
                "permalink": data.get("permalink"),
                "subreddit": data.get("subreddit"),
            })
            replies = data.get("replies")
            if isinstance(replies, dict):
                children = replies.get("data", {}).get("children", [])
                _flatten(children)
            elif isinstance(replies, list):
                _flatten(replies)

    _flatten(tree)
    return flat

def save_post(posts, subreddit, year, month):
    for p in posts:
        text = f"{p.get('title', '')} {p.get('selftext', '')}"
        if is_ai_related(text):
            link = f"https://reddit.com{p.get('permalink', '')}"
            save_row(
                p.get("id"), "post", p.get("selftext", ""), p.get("created_utc"),
                subreddit, year, month, link
            )

            # Fetch and flatten comment tree
            print(f" Fetching full comment tree for post {p.get('id')}")
            comments_flat = fetch_comment_tree(p.get("id"))
            for c in comments_flat:
                if is_ai_related(c.get("body", "")):
                    save_row(
                        c.get("id"), "comment_tree", c.get("body", ""),
                        c.get("created_utc"), subreddit, year, month,
                        f"https://reddit.com{c.get('permalink', '')}"
                    )

