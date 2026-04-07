import uuid
import qrcode
import os
import io

from flask_mail import Message
from flask import current_app
from .extensions import mail
from reportlab.lib.pagesizes import A6
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

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

def generate_ticket_pdf(ticket_id, name, day):

    # os.makedirs("tickets", exist_ok=True)

    qr_img = qrcode.make(ticket_id)

    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    # pdf_path = f"tickets/{ticket_id}.pdf"
    pdf_buffer = io.BytesIO()

    dates = {1: "29 de Mayo", 2: "30 de Mayo"}
    date_str = dates.get(int(day), f"Día {day}")

    c = canvas.Canvas(pdf_buffer, pagesize=A6)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(297/2, 420-60, "ENTRADA")

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(297/2, 420-80, f"Día {day} - {date_str}")

    c.setFont("Helvetica", 11)
    c.drawCentredString(297/2, 420-120, f"Caja Blanca 19:00 (apertura de puertas 18:30)")

    c.line(35, 420-145, 262, 420-145)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(35, 420-175, "Nombre:")
    c.setFont("Helvetica", 12)
    c.drawString(95, 420-175, name)

    # c.setFont("Helvetica", 12)
    # c.drawString(30, 330, f"Día {day}")
    # c.drawString(30, 310, f"Nombre: {name}")
    # c.drawString(30, 280, "Codigo de entrada:")
    # c.setFont("Helvetica", 10)
    # c.drawString(30, 260, f"{ticket_id}")

    qr_image = ImageReader(qr_buffer)
    c.drawImage(qr_image, (297/2)-(150/2), 60, width=150, height=150)
    # c.drawImage(qr_image, (297/2)-(120/2), 100, width=120, height=120)

    c.setFont("Helvetica", 9)
    c.drawCentredString(297/2, 50, f"ID: {ticket_id}")

    c.showPage()
    c.save()

    pdf_buffer.seek(0)

    return pdf_buffer

def send_ticket_email(email, ticket_id, pdf_buffer):

    msg = Message(
        subject="Tu entrada",
        recipients=[email],
    )

    msg.body = f"Id de tu entrada: {ticket_id}"

    # qr_path = os.path.join("static/qrcodes", f"{ticket_id}.png")

    # with open(pdf_path, "rb") as f:
        # msg.attach(
            # filename = "entrada.pdf",
            # content_type = "application/pdf",
            # data = f.read()
            # )

    msg.attach(
            filename = "entrada.pdf",
            content_type = "application/pdf",
            data = pdf_buffer.read()
            )

    mail.send(msg)
