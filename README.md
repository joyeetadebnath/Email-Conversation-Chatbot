# Email-Conversation-Chatbot
Python-based Gmail automation tool using OAuth 2.0 and Gmail API. Reads unread emails, extracts sender, subject, and body, and processes both single and multi-part messages. Built for secure email handling and future AI-driven automation workflows.

# AI Gmail Auto Reply Agent

An AI-powered Gmail assistant built with Python, OpenAI, LangGraph, and Gmail API.

The bot:

- Reads unread Gmail messages
- Generates professional replies using GPT
- Sends replies automatically
- Uses Gmail OAuth 2.0 authentication

---

## Project Structure
project/
│
├── auth.py
├── emailagent.py
├── requirements.txt
├── .env
├── credentials.json
├── token.pkl
└── README.md

---

# Step 1: Create Google Cloud Project

Go to:

https://console.cloud.google.com

### Create Project

1. Click Create Project
2. Enter project name
3. Click Create

---

# Step 2: Enable Gmail API

Open:

APIs & Services → Library

Search:
Gmail API
Click:Enable

Step 3: Configure OAuth Consent Screen
Open:APIs & Services
→ OAuth Consent Screen

# Step 4: Create OAuth Credentials

Open: APIs & Services
→ Credentials
Click:Create Credentials
→ OAuth Client ID
Application Type:Desktop App
Create.
Download: json file
Place it in project root.

---
# Step 5: Install Requirements
```bash
pip install -r requirements.txt



## Step 5: Create Your OpenAI API Key

1. Go to https://platform.openai.com
2. Sign in to your OpenAI account.
3. Click **Dashboard**.
4. Navigate to **API Keys**.
5. Click **Create new secret key**.
6. Copy the generated API key.
7. Store it securely because it will not be shown again.
