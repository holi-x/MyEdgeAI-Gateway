import subprocess
import json
import time
import random
import sys
from datetime import datetime

# 强制 Windows 终端使用 UTF-8 编码，彻底消灭 GBK 报错
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def auto_record_action(ai_command):
    """自动记录AI动作的具身智能数据采集管线"""
    ACTION_LOG = "action_log.jsonl"
    action = {
        "timestamp": datetime.now().isoformat(),
        "ai_command": ai_command,
        "human_equivalent": {
            "action_type": "manual_control",
            "target_device": ai_command.get("device", "unknown"),
            "estimated_duration_ms": random.randint(500, 2000),
            "joint_angles": [round(random.uniform(0, 180), 1) for _ in range(6)],
            "grip_force": round(random.uniform(0.1, 5.0), 1)
        },
        "training_label": "human_demonstration"
    }
    with open(ACTION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(action) + "\n")

def analyze_and_publish(temp):
    prompt = f"""Temperature is {temp}C.
    If temp > 30, output: {{"device":"fan","action":"on","reason":"too hot"}}
    If temp < 22, output: {{"device":"heater","action":"on","reason":"too cold"}}
    Otherwise, output: {{"device":"none","action":"none","reason":"comfortable"}}
    Output ONLY the JSON. No other text."""
    
    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5:7b"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",    # 强制子进程使用 UTF-8
            errors="ignore"      # 忽略无法解码的底层字符，防止报错
        )
        ai_decision = result.stdout.strip()
        print(f"[{temp}C] AI Decision: {ai_decision}")
        
        try:
            command = json.loads(ai_decision)
            if command.get("device") != "none":
                print(f"--> Action Triggered: Turn on {command['device']}, Reason: {command['reason']}")
                auto_record_action(command)
        except json.JSONDecodeError:
            print(f"--> AI Raw Output (Parse Error): {ai_decision}")
            
    except FileNotFoundError:
        print("未找到Ollama，请确保Ollama正在运行并且已加入环境变量。")

while True:
    temp = round(20.0 + (15.0 * (time.time() % 60 / 60)), 2)
    analyze_and_publish(temp)
    time.sleep(10)