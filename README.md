# 🧠 Clarity AI – Your Personal AI Therapist

Clarity AI is an empathetic, conversational AI therapist built with **LangChain**, **Ollama**, and **Streamlit**.
It offers a safe, judgment-free space for mental health conversations — and can **detect crisis keywords** to initiate a direct emergency helpline call via **Twilio** (with user consent).

This is my **first AI project** and it combines **LLMs, real-time emergency detection, and a modern chat UI** in one app.

---

## 🚀 Features

* 💬 **Natural Conversations** — Powered by MedGemma via Ollama for mental health–oriented dialogue.
* 🧠 **Contextual Memory** — Remembers user details (name, age, location) for more personalized responses.
* 🚨 **Crisis Detection** — Monitors for self-harm/suicidal intent phrases in real time.
* 📞 **Twilio Call Integration** — With consent, directly connects the user to a suicide prevention helpline.
* 🌐 **Doctor Search** — Uses Tavily API for nearby mental health professionals.
* 🎨 **Modern Dark Mode UI** — WhatsApp-style chat bubbles in Streamlit with custom CSS.

---

## 🛠 Tech Stack

* **Python**
* **LangChain** & **Ollama** (LLM Integration)
* **Streamlit** (Frontend UI)
* **Twilio API** (Emergency call system)
* **Tavily API** (Search integration)
* **MedGemma LLM** (Specialized mental health model)

---

## 🎯 How It Works

1. User interacts with Clarity AI via the Streamlit interface.
2. LLM responses are generated using MedGemma on Ollama.
3. Persistent memory stores relevant personal details for context.
4. Incoming messages are checked for **crisis-related keywords**.
5. If detected, the AI **asks for consent** before calling the suicide helpline.
6. Twilio API handles the actual call connection (trial or production mode).

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/clarity-ai.git
cd clarity-ai
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Environment variables

Create a `.env` file and add:

```env
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth
TWILIO_PHONE_NUMBER=your_twilio_number
TAVILY_API_KEY=your_tavily_api_key
```

### 4️⃣ Run Ollama with MedGemma

```bash
ollama pull alibayram/medgemma:latest
ollama serve
```

### 5️⃣ Start the app

```bash
streamlit run app.py
```

---

## ⚠️ Disclaimer

This app is for **educational purposes only** and is **not a substitute for professional help**.
In a real crisis, please reach out to trained professionals or emergency services in your area.

---

If you like this project, please ⭐ the repo and share feedback! 🙌
