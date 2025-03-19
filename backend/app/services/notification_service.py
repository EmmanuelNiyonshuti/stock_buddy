"""
notification services.
"""
import os
from twilio.rest import Client
from dotenv import load_dotenv
from app.models import notification
from app import db


load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = os.environ["TWILIO_PHONE_NBR"]

client = Client(account_sid, auth_token)

def send_sms(to, msg_body):
    """Send an SMS notification via Twilio"""
    notification = Notification(
                                recipient=to,
                                message=msg_body,
                                channel="SMS",
                                status="Pending"
                                )
    db.session.add(notification)
    db.session.commit()
    try:
        message = client.messages.create(
            body=msg_body,
            from_=twilio_phone_number,
            to=to,
            )
        notification.status = "Sent"
        db.session.commit()
        return {"success": True, "message": "SMS sent successfully"}
    except Excepion as e:
        notification.status = "Failed"
        return {"success": False, "error": str(e)}
    finally:
        db.session.commit()
