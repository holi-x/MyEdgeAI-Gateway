# 🛡️ Project Sovereign: Private AI Edge Gateway

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![AI](https://img.shields.io/badge/AI-Qwen_2.5_7B-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Not just using AI. Defining the rules under which AI interacts with the physical world.**

Project Sovereign is a fully private, offline, and auditable edge AI system that controls physical devices via local LLMs. Designed for the next generation of Embodied AI and trusted automation, it ensures **zero cloud dependency** and **100% decision traceability**.

---

## 🚀 Core Features (Why this matters)

*   **Absolute Privacy**: All data (sensor inputs, AI reasoning) is processed locally. No data leaks to OpenAI or any cloud API.
*   **Auditable Decision Pipeline**: Every AI command generates a human-readable JSON log with a complete evidence chain.
*   **Embodied AI Data Generator**: Automatically converts AI decisions into human-equivalent physical movement data (joint angles, duration, grip force), ready for robotics training.
*   **Automated Analytics**: Built-in report generator to quantify system performance and AI safety.

---

## 🏗️ System Architecture

```text
[Physical Sensor] -> (Temperature Data)
       │
       ▼
[Local LLM Engine] -> (Qwen 2.5:7b) -> Analyzes data & outputs strict JSON
       │
       ▼
[Action Dispatcher] -> Interprets JSON (e.g., {"device":"fan", "action":"on"})
       │
       ├──> [Embodied Data Pipeline] -> Generates action_log.jsonl (Training Data)
       │
       └──> [Analytics Engine] -> Generates ACTION_REPORT.md (Audit & Metrics)
       📊 Live System Metrics
 
Check out the auto-generated ACTION_REPORT.md to see the latest system performance.
• Total Auditable AI Decisions: Accumulating in real-time
• Human-Equivalent Action Mapping: Active
• Data Privacy Level: Air-gapped / Offline 
 
💻 Quick Start
 
Prerequisites
• Python 3.10+
• Ollama installed and running locally. 
1. Install Dependencies
git clone https://github.com/holi-x/MyEdgeAI-Gateway.git
cd MyEdgeAI-Gateway
pip install -r requirements.txt  # (If you don't have this, just pip install paho-mqtt)
 
2. Pull the Local Brain
ollama run qwen2.5:7b
 
3. Run the Sovereign Core
python ai_mqtt_controller.py
 
(The system will start simulating physical data, generating AI decisions, and recording embodied training data automatically.)
 
4. Generate Analytics Report
python analyze_log.py
 
 
🗺️ Roadmap
[x] v0.1 (Current): Offline LLM integration, physical action simulation, and automated data logging.
[ ] v0.2: Real MQTT hardware integration (Raspberry Pi / Smart Home).
[ ] v0.3: Multi-modal input (Vision + Audio).
[ ] v0.4: Decentralized identity and tokenized decision assets. 
 
🤝 Contact & Consulting
 
I help organizations achieve AI Sovereignty and build privacy-first embodied AI pipelines.
• Open for Collaboration / Hiring / Consulting.
• Reach out via GitHub Issues or Email: [hongxiao-liu@outlook.com]