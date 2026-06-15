import feedparser
import json
import time
import subprocess
from datetime import datetime

ARXIV_RSS_URL = "https://rss.arxiv.org/rss/cs.AI"

def fetch_latest_papers():
    feed = feedparser.parse(ARXIV_RSS_URL)
    papers = []
    for entry in feed.entries[:3]:
        papers.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link,
            "published": entry.published
        })
    return papers

def analyze_paper(paper):
    prompt = f"""You are an AI research analyst. Analyze this paper and output ONLY a JSON with this structure:
{{
    "title": "{paper['title']}",
    "core_insight": "One sentence summarizing the core breakthrough",
    "disruptive_potential": "high/medium/low",
    "why_matters": "Why this could change the AI landscape in 5 years",
    "tags": ["tag1", "tag2"]
}}
Paper summary: {paper['summary']}
Output ONLY the JSON. No other text."""

    result = subprocess.run(
        ["ollama", "run", "qwen3:4b"],
        input=prompt,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

while True:
    print(f"[{datetime.now()}] Fetching latest AI papers...")
    papers = fetch_latest_papers()
    
    for paper in papers:
        analysis = analyze_paper(paper)
        record = {
            "timestamp": datetime.now().isoformat(),
            "paper": paper,
            "ai_analysis": analysis
        }
        
        with open("/home/lhx/MyEdgeAI-Gateway/intelligence/intel_log.jsonl", "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
        print(f"Analyzed: {paper['title'][:80]}...")
    
    print("Waiting 1 hour before next fetch...")
    time.sleep(3600)