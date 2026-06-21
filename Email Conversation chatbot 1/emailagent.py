# Step 1: Basic Setup - Load token & Connect Gmail API

import pickle
import base64
import os
from langchain_openai import ChatOpenAI
import getpass

OPENAI_API_KEY = getpass.getpass(
    "Enter your OpenAI API Key: "
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)


from typing import TypedDict
from email.mime.text import MIMEText

from googleapiclient.discovery import build


# Load token
# with open("token.pkl", "rb") as token:
#     creds = pickle.load(token)
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file(
        "Give you secret key",
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    return creds

creds = authenticate_gmail()

service = build("gmail", "v1", credentials=creds)
# Gmail service
service = build("gmail", "v1", credentials=creds)


# Step 2: Get unread emails
def get_unread_emails(max_results=5):
    results = service.users().messages().list(
        userId="me",
        labelIds=["UNREAD"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    email_list = []

    for msg in messages:
        subject, sender, body = read_email(msg["id"])

        email_list.append({
            "id": msg["id"],
            "from": sender,
            "subject": subject,
            "body": body
        })

    return email_list

def read_email(msg_id):
    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    payload = msg.get("payload", {})
    headers = payload.get("headers", [])

    subject = ""
    sender = ""

    for header in headers:
        name = header.get("name", "").lower()

        if name == "subject":
            subject = header.get("value", "")

        elif name == "from":
            sender = header.get("value", "")

    # Decode email body
    body = ""

    try:
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data")

                    if data:
                        data += "=" * (-len(data) % 4)
                        body = base64.urlsafe_b64decode(data).decode(
                            "utf-8",
                            errors="ignore"
                        )
                        break
        else:
            data = payload.get("body", {}).get("data")

            if data:
                data += "=" * (-len(data) % 4)
                body = base64.urlsafe_b64decode(data).decode(
                    "utf-8",
                    errors="ignore"
                )

    except Exception as e:
        body = f"Could not decode email body: {e}"

    return subject, sender, body


# Step 3: Send Email
def send_email(to, subject, body):
    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    print(f"Email sent to {to}")


# Step 4: State Definition
class EmailState(TypedDict):
    sender: str
    subject: str
    body: str
    reply: str


def generate_reply(state: EmailState):
    prompt = f"""
You are a professional email assistant.

Write a concise, professional reply.

Subject:
{state['subject']}

Email:
{state['body']}

Rules:
- Be polite
- Be concise
- Do not invent facts
- If information is missing,
  ask for clarification
"""

    response = llm.invoke(prompt)

    return {"reply": response.content}
def send_reply(state: EmailState):
    send_email(
        state["sender"],
        f"Re: {state['subject']}",
        state["reply"]
    )
    return state
from langgraph.graph import StateGraph

builder = StateGraph(EmailState)

builder.add_node("generate_reply", generate_reply)
builder.add_node("send_reply", send_reply)

builder.set_entry_point("generate_reply")
builder.add_edge("generate_reply", "send_reply")
builder.set_finish_point("send_reply")

graph = builder.compile()
graph

emails = get_unread_emails()

print(f"Found {len(emails)} unread emails")

for email in emails:
    result = graph.invoke({
        "sender": email["from"],
        "subject": email["subject"],
        "body": email["body"],
        "reply": ""
    })

    print("Reply sent:")
    print(result["reply"])