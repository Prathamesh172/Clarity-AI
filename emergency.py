# emergency.py
import re
from twilio.rest import Client
import os

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
SUICIDE_HELPLINE_NUMBER = "+919152987821"  # India helpline

# Detect crisis in text
def check_for_emergency(text):
    emergency_keywords = [
        "suicide", "kill myself", "end my life", "can't go on", "take my life",
        "self harm", "hurt myself", "want to die"
    ]
    return any(kw in text.lower() for kw in emergency_keywords)

# Format phone number to E.164 for India (+91)
def format_phone_number(phone):
    phone = re.sub(r"\D", "", phone)
    if not phone.startswith("91"):
        phone = "91" + phone
    return "+" + phone

# Make Twilio call
def make_emergency_call(user_phone):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return "⚠️ Twilio credentials are missing."

    user_phone = format_phone_number(user_phone)
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            to=user_phone,
            from_=TWILIO_PHONE_NUMBER,
            url=f"http://twimlets.com/forward?PhoneNumber={SUICIDE_HELPLINE_NUMBER}"
        )
        return f"✅ Emergency call initiated."
    except Exception as e:
        return f"⚠️ Error making call: {str(e)}"
