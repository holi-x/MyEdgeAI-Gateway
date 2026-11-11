import json
import os

LOG_FILE = "action_log.jsonl"
REPORT_FILE = "ACTION_REPORT.md"

def generate_report():
    if not os.path.exists(LOG_FILE):
        print("日志文件不存在，请先运行主程序生成数据。")
        return

    total_actions = 0
    fan_on_count = 0
    heater_on_count = 0
    total_duration = 0

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                total_actions += 1
                
                device = data["ai_command"].get("device", "none")
                if device == "fan":
                    fan_on_count += 1
                elif device == "heater":
                    heater_on_count += 1
                    
                total_duration += data["human_equivalent"]["estimated_duration_ms"]
            except:
                pass

    avg_duration = total_duration / total_actions if total_actions > 0 else 0

    report = f"""# Sovereign System - Action Automation Report

## Overview
This report is auto-generated from the `action_log.jsonl` data pipeline.

- **Total AI Decisions Recorded:** {total_actions}
- **Fan Activations (Too Hot):** {fan_on_count}
- **Heater Activations (Too Cold):** {heater_on_count}
- **Average Human Equivalent Duration:** {avg_duration:.2f} ms

## Value Proposition
Every action recorded here represents a fully auditable AI decision mapped to human-equivalent physical movements. This dataset is ready to be used for training embodied AI agents (robotics) in a safe, traceable manner.

*Report generated automatically.*
"""
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"报告已生成: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()