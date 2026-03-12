import uuid
import qrcode
import os

from flask_mail import Message
from flask import current_app
from .extensions import mail

def generate_ticket_id():
    return str(uuid.uuid4())

def generate_qr_code(ticket_id):

    folder = "static/qrcodes"
    os.makedirs(folder, exist_ok=True)

    filename = f"{ticket_id}.png"
    filepath = os.path.join(folder, filename)

    img = qrcode.make(ticket_id)
    img.save(filepath)

    return filepath

def send_ticket_email(email, ticket_id):

    msg = Message(
        subject="Tu entrada",
        recipients=[email],
    )

    msg.body = f"Id de tu entrada: {ticket_id}"

    qr_path = os.path.join("static/qrcodes", f"{ticket_id}.png")

    with open(qr_path, "rb") as f:
        msg.attach(
            filename = f"{ticket_id}.png",
            content_type = "image/png",
            data = f.read()
            )

    mail.send(msg)
