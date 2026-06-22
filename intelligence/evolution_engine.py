import subprocess
import json
import os
from datetime import datetime

EVOLUTION_LOG = "/home/lhx/MyEdgeAI-Gateway/intelligence/evolution_log.jsonl"

def get_latest_knowledge():
    """从知识库中检索最新的情报，作为进化的依据"""
    # 简化版：直接读取最新的一条情报日志
    log_path = "/home/lhx/MyEdgeAI-Gateway/intelligence/intel_log.jsonl"
    if not os.path.exists(log_path):
        return "No new knowledge."
    
    lines = []
    with open(log_path, "r") as f:
        lines = f.readlines()
    
    if not lines:
        return "No new knowledge."
    
    # 取最新的一条
    latest = json.loads(lines[-1])
    return json.dumps(latest.get("ai_analysis", {}))

def generate_new_rule(new_knowledge):
    """让AI基于新知识，提出一条新的行为规则或对旧规则的修改建议"""
    prompt = f"""You are the evolution engine of a private AI sovereignty system.

Current new knowledge: {new_knowledge}

Based on this knowledge, propose ONE new rule or modification to the system's behavior.
Output ONLY a JSON with this exact structure:
{{
    "rule_name": "short name of the new rule",
    "rule_description": "what the new rule does",
    "action": "add|modify|delete",
    "reason": "why this rule is needed based on the new knowledge"
}}

If the knowledge doesn't warrant any rule change, output:
{{
    "rule_name": "none",
    "action": "none",
    "reason": "no significant change needed"
}}

Output ONLY the JSON. No other text."""

    result = subprocess.run(
        ["ollama", "run", "qwen3:4b"],
        input=prompt,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def log_evolution(rule):
    """记录每一次进化"""
    record = {
        "timestamp": datetime.now().isoformat(),
        "rule": rule
    }
    with open(EVOLUTION_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")
    print(f"[{record['timestamp']}] Evolution logged: {rule.get('rule_name', 'unknown')}")

# 主循环
print(f"[{datetime.now()}] Evolution engine checking for new knowledge...")
new_knowledge = get_latest_knowledge()
print(f"Latest knowledge: {new_knowledge[:200]}...")

new_rule_json = generate_new_rule(new_knowledge)
print(f"AI proposed rule: {new_rule_json}")

try:
    new_rule = json.loads(new_rule_json)
    log_evolution(new_rule)
    if new_rule.get("action") != "none":
        print(f"--> New rule adopted: {new_rule.get('rule_name')}")
except json.JSONDecodeError:
    print("--> AI output was not valid JSON, skipping this cycle.")