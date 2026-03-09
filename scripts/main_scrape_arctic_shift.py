import time
from src.data_collection.arctic_shift import (
    SUBREDDITS,
    month_ranges,
    fetch_data,
    save_post
)

def main():

    for subreddit in SUBREDDITS:

        for after, before, year, month in month_ranges(2018,1,2025,12):

            print(f"\nFetching r/{subreddit} {year}-{month:02d} posts")

            posts = fetch_data(subreddit, after, before, "posts")

            save_post(posts, subreddit, year, month)

            print(f"Finished r/{subreddit} {year}-{month:02d}")
            time.sleep(2)

    print("Data collection complete.")


if __name__ == "__main__":
    main()