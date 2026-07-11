import os

import resend
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resend.api_key = os.environ["RESEND_API_KEY"]

AUDIENCE_ID = os.environ["RESEND_AUDIENCE_ID"]
CONTACT_EMAIL = os.environ["CONTACT_EMAIL"]


class WaitlistRequest(BaseModel):
    email: str


class ContactRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    message: str


@app.post("/waitlist")
def waitlist(request: WaitlistRequest):
    resend.Contacts.create({
        "email": request.email,
        "audience_id": AUDIENCE_ID,
    })

    return {"success": True}


@app.post("/contact")
def contact(request: ContactRequest):
    resend.Emails.send({
        "from": "Pelion <resend@pelionlearn.com>",
        "to": [CONTACT_EMAIL],
        "reply_to": request.email,
        "subject": f"New Contact Form - {request.first_name} {request.last_name}",
        "html": f"""
        <h2>New Contact Form Submission</h2>

        <p><strong>Name:</strong> {request.first_name} {request.last_name}</p>
        <p><strong>Email:</strong> {request.email}</p>

        <h3>Message</h3>
        <p>{request.message.replace("\n", "<br>")}</p>
        """,
    })

    return {"success": True}