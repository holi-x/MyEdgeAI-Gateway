import subprocess
import json
import time
import datetime
import paho.mqtt.client as mqtt

# MQTT Setup for paho-mqtt 2.x
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "edge_ai_brain")
client.connect("localhost", 1883, 60)
client.loop_start()

def analyze_and_publish(temp):
    prompt = f"""Temperature is {temp}C.
    If temp > 30, output: {{"device":"fan","action":"on","reason":"too hot"}}
    If temp < 22, output: {{"device":"heater","action":"on","reason":"too cold"}}
    Otherwise, output: {{"device":"none","action":"none","reason":"comfortable"}}
    Output ONLY the JSON. No other text."""

    result = subprocess.run(
        ["ollama", "run", "qwen3:4b"],
        input=prompt,
        capture_output=True,
        text=True
    )

    ai_decision = result.stdout.strip()
    timestamp = datetime.datetime.now().isoformat()

    # Build complete audit record
    audit_record = {
        "timestamp": timestamp,
        "input": {"temperature": temp},
        "ai_prompt": prompt,
        "ai_raw_output": ai_decision
    }

    print(f"[{timestamp}] Temp: {temp}C -> AI: {ai_decision}")

    try:
        command = json.loads(ai_decision)
        audit_record["action"] = command
        if command.get("device") != "none":
            client.publish("home/devices/control", json.dumps(command))
            print(f"--> MQTT Sent: {command}")
    except json.JSONDecodeError:
        audit_record["action"] = {"error": "JSON parse failed", "raw": ai_decision}
        print(f"--> AI Raw: {ai_decision}")

    # Write audit log to file
    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(audit_record) + "\n")

# Main loop
print("Project Sovereign - AI Edge Gateway Starting...")
print("Audit log: audit_log.jsonl")
print("-" * 50)

while True:
    temp = round(20.0 + (15.0 * (time.time() % 60 / 60)), 2)
    analyze_and_publish(temp)
    time.sleep(10)