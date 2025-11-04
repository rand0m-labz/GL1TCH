# architecture.md

# 🧠 GL1TCH Agent – Architecture Overview

### 🚀 Overview

The **GL1TCH Agent** is an automated AI responder workflow built using **Flask**, **n8n**, **OpenAI**, and **HTTP webhooks**, fully deployed via **Docker** on **Render**.  
It listens for incoming prompts from web requests or Telegram messages, forwards them through an n8n LLM chain, and returns a structured JSON response with Gl1tch's personality baked in.

---

## 🧩 Core Components

### **1. Webhook Node**

- **Purpose:** Entry point for all incoming POST requests.
- **Local URL Pattern:**
```
  http://localhost:5678/webhook-test/gl1tch-test
```
- **Request Body Example:**
```json
  {
    "prompt": "Gl1tch, are you online?"
  }
```

- **Output:**  
  The webhook captures the JSON payload and passes it to the **HTTP Request** node.

---

### **2. Webhook Node (n8n-gl1tch)**

- **Purpose:** Entry point for all incoming POST requests in production.
- **Production URL:**
```
  https://n8n-gl1tch.onrender.com/webhook/gl1tch-test
```
- **Request Body Example:**
```json
  {
    "prompt": "Gl1tch, analyze this text..."
  }
```
- **Output:**  
  Forwards the JSON body into the LLM workflow, connecting Flask (gl1tch-agent) to n8n (n8n-gl1tch).

---

### **3. Basic LLM Chain**

- **Purpose:** Passes the user's prompt into an OpenAI Chat Model and retrieves a response.
- **Input Source:** `HTTP Request`
- **Prompt Expression:**
```handlebars
  {{$json.body.prompt}}
```
- **Chat Messages:** None (single-prompt mode)
- **Model Connected:** `OpenAI Chat Model1`
- **Output:** Returns a JSON object containing the AI's response, e.g.:
```json
  {
    "text": "Hey there, GL1TCH is online ⚡"
  }
```

---

### **4. OpenAI Chat Model**

- **Purpose:** Processes the text prompt via OpenAI's API (GPT-4 or GPT-5 model).
- **Response Type:** Free-form text
- **Output Field:** `text` (used by the next node)

---

### **5. Respond to Webhook**

- **Purpose:** Sends a structured response back to the requester.
- **Respond With:** JSON
- **Response Body:**
```json
  {
    "reply": "{{ $json.text || 'No response generated' }}"
  }
```

- **Example Response:**
```json
  {
    "reply": "Yo, GL1TCH here — system stable and listening 👾"
  }
```

---

## 🛠️ Workflow Summary

| Step | Node                   | Role                         | Input               | Output               |
| ---- | ---------------------- | ---------------------------- | ------------------- | -------------------- |
| 1️⃣   | **Webhook**            | Receives POST request        | User prompt         | JSON body            |
| 2️⃣   | **HTTP Request**       | Forwards to LLM chain        | Webhook output      | Same data            |
| 3️⃣   | **Basic LLM Chain**    | Builds prompt & calls OpenAI | `$json.body.prompt` | AI response          |
| 4️⃣   | **OpenAI Chat Model**  | Generates completion         | Prompt text         | `{ "text": "..." }`  |
| 5️⃣   | **Respond to Webhook** | Returns output               | LLM output          | `{ "reply": "..." }` |

---

## 🧪 Test Command
```powershell
Invoke-WebRequest -Uri "https://n8n-gl1tch.onrender.com/webhook/gl1tch-test" `
-Method POST -Body '{"prompt":"Gl1tch, are you online?"}' `
-ContentType "application/json"
```

**Expected Output:**
```json
{
  "reply": "Hey there! Gl1tch reporting in ⚡"
}
```

---

## 🧰 Environment Variables (`.env`)
```ini
# Core Keys
OPENAI_API_KEY=your_api_key_here

# Agent Info
AGENT_NAME=GL1TCH
AGENT_PORT=8080
GL1TCH_API_URL=https://gl1tch-agent.onrender.com
WEBHOOK_URL=https://n8n-gl1tch.onrender.com/webhook/gl1tch-test

# Optional Future Variables
GL1TCH_MODEL=gpt-5
SERVICE_TYPE=agent
```

---

## 🌐 Future Enhancements

- 🧩 Add personality profiles for Gl1tch (sarcasm, analysis, humor)
- 🕹️ Integrate external APIs for real data (crypto, weather, etc.)
- 💾 Log chat history to MongoDB or Supabase
- 🤖 Add Telegram and X(Twitter) bot layers
- 🧠 Introduce persistent memory between sessions
- ⚙️ Add health monitoring & uptime checks for both Render services