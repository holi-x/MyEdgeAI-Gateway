import subprocess
import json
import time
import paho.mqtt.client as mqtt

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
    print(f"[{temp}C] AI Decision: {ai_decision}")
    
    try:
        command = json.loads(ai_decision)
        if command.get("device") != "none":
            client.publish("home/devices/control", json.dumps(command))
            print(f"--> MQTT Sent: Turn on {command['device']}, Reason: {command['reason']}")
    except json.JSONDecodeError:
        print(f"--> AI Raw Output: {ai_decision}")

while True:
    temp = round(20.0 + (15.0 * (time.time() % 60 / 60)), 2)
    analyze_and_publish(temp)
    time.sleep(10)
