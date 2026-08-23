import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]


async def send_email(to: str, subject: str, content: str):
    params: resend.Emails.SendParams = {
        "from": "Pelion <noreply@pelionlearn.com>",
        "to": [to],
        "subject": subject,
        "html": content,
    }

    email: resend.Emails.SendResponse = resend.Emails.send(params)

    return email
