# 🧩 GL1TCH System Architecture

## Overview
GL1TCH is a modular AI agent designed to run inside Docker and communicate with **n8n** for automation and workflow control.  
It starts as a lightweight Flask service but can evolve into any specialized role (analysis, automation, or content generation).

---

## 🧱 Core Components

### 1. **Agent Layer (Flask)**
Handles HTTP requests, runs AI logic, and returns responses.  
Located in `agent/main.py`.

### 2. **n8n Workflow Engine**
Acts as Gl1tch’s “brain network.”  
- Triggers agent functions via webhooks or HTTP nodes.  
- Handles automation tasks like posting, data fetching, or message routing.  

### 3. **Scripts Layer**
Includes startup scripts like `entrypoint.sh` for container initialization.

### 4. **Config Layer**
All configuration and environment handling lives in `agent/config.py` + `.env`.

---

## 🐳 Container Layout
| Container | Port | Role |
|------------|------|------|
| gl1tch     | 8080 | Agent API |
| n8n        | 5678 | Workflow Engine |

---

## 🔁 Data Flow