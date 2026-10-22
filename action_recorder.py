import json
import random
from datetime import datetime

ACTION_LOG = "action_log.jsonl"

def record_action(ai_command):
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
    with open(ACTION_LOG, "a") as f:
        f.write(json.dumps(action) + "\n")
    return action

if __name__ == "__main__":
    test_command = {"device": "fan", "action": "on", "reason": "too hot"}
    result = record_action(test_command)
    print("Recorded action:")
    print(json.dumps(result, indent=2))