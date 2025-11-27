import smtplib
from fastapi import HTTPException, status
from email.message import EmailMessage
from .. config import EMAIL_HOST, EMAIL_PORT,EMAIL_USER,EMAIL_PASSWORD,EMAIL_FROM,EMAIL_USE_TLS

def send_otp_email(to_email : str, otp: str):
    """
    this function send otp from a specific mail
    """
    subject = "Your OTP Code"
    body = f"""
    Assalamu Alaikum,

    Your OTP code is: {otp}

    If you did not fequest this code, pleace ignore this email.

    best regards,
    AYNI WELNESS
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(body)

    try: 
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if EMAIL_USE_TLS:
            server.starttls()

        server.login(EMAIL_USER, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

    except :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="dosn't abole to send email"
        )