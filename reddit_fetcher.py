from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

import openai
from openai import OpenAI

client = OpenAI(api_key=api_key)


# reddit_fetcher.py
import praw

# === CONFIGURATION ===
# Ensure you have the following in your .env file:
# REDDIT_CLIENT_ID=your_client_id
# REDDIT_CLIENT_SECRET=your_client_secret
# REDDIT_USER_AGENT=your_user_agent

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

reddit.read_only = True  # ✅ force read-only mode

def extract_product_info(title, comment):
    prompt = f"""
You are analyzing Reddit posts to identify product trends and guide new product development.

Title: {title}
Comment: {comment}

Based on this content, understand the content in the following format:

{{
  "products": [list of product names],
  "brands": [list of brand names],
  "notable_attributes": [list of traits users appreciate: e.g. 'durable', 'lifetime warranty', 'repairable'],
  "trend_insight": "short summary of why this product/brand is being praised",
  "product_recommendation": "what type of product should the user consider making, and why"
}}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

def fetch_top_posts(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=limit):
        posts.append({
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "num_comments": post.num_comments
        })
    return posts

def fetch_top_comments(subreddit_name, post_limit=10, comment_limit=1):
    subreddit = reddit.subreddit(subreddit_name)
    posts_with_comments = []

    for post in subreddit.hot(limit=post_limit):
        post.comments.replace_more(limit=0)
        top_comments = post.comments[:comment_limit]

        posts_with_comments.append({
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "num_comments": post.num_comments,
            "top_comments": [comment.body for comment in top_comments]
        })

    return posts_with_comments

if __name__ == "__main__":
    results = fetch_top_comments("BuyItForLife", post_limit=10, comment_limit=1)
    combined_context = ""

    for post in results:
        title = post["title"]
        top_comment = post["top_comments"][0] if post["top_comments"] else ""
        combined_context += f"Title: {title}\nComment: {top_comment}\n\n"

    prompt = f"""
You are analyzing multiple Reddit posts to identify product trends and advise a new business owner.

Here are several Reddit posts and their top comments:

{combined_context}

Write a short, friendly, and insightful paragraph that summarizes:
- What kinds of products and brands are trending
- What traits successful products have in common
- What kind of product the user should consider creating and why

Make it suitable for directly displaying in a frontend UI.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    print("\n🔍 AI Combined Insight:")
    print(response.choices[0].message.content.strip())