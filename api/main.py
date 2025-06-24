from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/request-demo")
async def request_demo(
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(""),
    message: str = Form("")
):
    content = f"""
    📩 New demo request:

    👤 Name: {name}
    ✉️ Email: {email}
    🏢 Company: {company}
    📝 Message: {message}
    """

    msg = EmailMessage()
    msg["Subject"] = "New Demo Request"
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_USER
    msg.set_content(content)

    try:
        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=GMAIL_USER,
            password=GMAIL_APP_PASSWORD,
        )
        return {"status": "success", "message": "Demo request sent!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}