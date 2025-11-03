# 🧠 GL1TCH Agent – Architecture Overview

### 🚀 Overview

The **GL1TCH Agent** is an automated AI responder workflow built using **n8n**, **OpenAI**, and **HTTP webhooks**.  
It listens for incoming prompts via a webhook, processes the message through an LLM chain, and returns a formatted JSON response.

---

## 🧩 Core Components

### **1. Webhook Node**

- **Purpose:** Entry point for all incoming POST requests.
- **URL Pattern:**
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

### **2. HTTP Request Node**

- **Purpose:** Acts as a relay or pre-processor.  
  (Used to transform, forward, or log incoming requests before LLM handling.)
- **Configured Method:** `POST`
- **Connected To:** `Basic LLM Chain1`
- **Input Mapping:**  
  Reads the full body payload from the Webhook node:
  ```json
  { "body": { "prompt": "..." } }
  ```

---

### **3. Basic LLM Chain**

- **Purpose:** Passes the user’s prompt into an OpenAI Chat Model and retrieves a response.
- **Input Source:** `HTTP Request`
- **Prompt Expression:**
  ```handlebars
  {{$json.body.prompt}}
  ```
- **Chat Messages:** None (single-prompt mode)
- **Model Connected:** `OpenAI Chat Model1`
- **Output:** Returns a JSON object containing the AI’s response, e.g.:
  ```json
  { "text": "Hey there, GL1TCH is online ⚡" }
  ```

---

### **4. OpenAI Chat Model**

- **Purpose:** Processes the text prompt via OpenAI’s API (GPT-4 or GPT-5 model).
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
Invoke-WebRequest -Uri "http://localhost:5678/webhook-test/gl1tch-test" `
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

```
OPENAI_API_KEY=your_api_key_here
```

Optional future variables:

```
GL1TCH_MODEL=gpt-5
GL1TCH_WEBHOOK_URL=http://localhost:5678/webhook-test/gl1tch-test
```

---

## 🌐 Future Enhancements

- 🧩 Add personality profiles for Gl1tch (sarcasm, analysis, humor)
- 🕹️ Integrate external APIs for real data (crypto, weather, etc.)
- 💾 Log chat history to MongoDB or Supabase
- 🧠 Introduce memory between sessions
