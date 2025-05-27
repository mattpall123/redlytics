# 🧠 Redlytics

Redlytics is an AI-powered Reddit trend analyzer that helps makers, startups, and indie founders discover what products communities care about — and what to build next.

It scrapes hot posts and top comments from any subreddit, processes the data with OpenAI, and returns a product insight based on real user discussion and sentiment.

---

## Tech Stack

**Frontend:** Next.js, React, TailwindCSS, Pixel RetroUI  
**Backend:** FastAPI, Python, PRAW (Reddit API), OpenAI GPT-3.5  
**Dev Tools:** VS Code, Vercel (frontend), Railway/Render (backend)

---

## Getting Started

## Frontend Setup

```bash
npm install
npm run dev
# or: yarn dev / pnpm dev / bun dev

Backend Setup (Python + FastAPI)
1.	Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install backend dependencies
"pip install -r requirements.txt" 

3. Create a .env file in the root directory and add:
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
OPENAI_API_KEY=your_openai_key

4. Start backend server
uvicorn api:app --reload

Features
	•	Analyze trending posts + comments from any subreddit
	•       Generate AI-powered product creation recommendations
	•	Identify common product traits, brands, and ideas
	•	 Real-time frontend with animated UI and progress feedback




