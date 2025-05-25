from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from reddit_fetcher import fetch_top_comments, client
import os

app = FastAPI()

# Optional: Enable frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all or replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/insight")
def get_insight(subreddit: str = Query(default="BuyItForLife")):
    try:
        results = fetch_top_comments(subreddit, post_limit=10, comment_limit=1)
    except Exception as e:
        return {"error": f"Failed to fetch from subreddit '{subreddit}': {str(e)}"}

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

    insight = response.choices[0].message.content.strip()
    return {"insight": insight}