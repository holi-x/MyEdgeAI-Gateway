import chromadb
import json
import os

client = chromadb.PersistentClient(path="/home/lhx/MyEdgeAI-Gateway/knowledge_base")
collection = client.get_or_create_collection("sovereign_knowledge")

log_path = "/home/lhx/MyEdgeAI-Gateway/intelligence/intel_log.jsonl"

if os.path.exists(log_path):
    with open(log_path, "r") as f:
        for line in f:
            record = json.loads(line)
            paper = record.get("paper", {})
            analysis = record.get("ai_analysis", "{}")
            
            doc_id = paper.get("link", str(hash(line)))
            document = f"Title: {paper.get('title', '')}\nSummary: {paper.get('summary', '')}\nAI Analysis: {analysis}"
            
            collection.add(
                documents=[document],
                ids=[doc_id]
            )
    
    print(f"Knowledge base updated. Total documents: {collection.count()}")
else:
    print("No intelligence log found. Run arxiv_crawler.py first.")