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
    hours = {1: "Caja Blanca 19:00 (apertura de puertas 18:30)", 2: "Caja Blanca 18:30 (apertura de puertas 18:00)"}
    hours_str = hours.get(int(day), f"")

    c.drawCentredString(297/2, 420-120, hours_str)

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
    c.drawImage(qr_image, (297/2)-(150/2), 75, width=150, height=150)
    # c.drawImage(qr_image, (297/2)-(120/2), 100, width=120, height=120)

    c.setFont("Helvetica", 9)
    c.drawCentredString(297/2, 65, f"ID: {ticket_id}")

    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawCentredString(297/2, 45, "Asoc. Cultural sin Ánimo de Lucro")
    c.drawCentredString(297/2, 35, "Donaciones en efectivo bienvenidas")
    c.drawCentredString(297/2, 25, "@telonautasteatro")


    c.showPage()
    c.save()

    pdf_buffer.seek(0)

    return pdf_buffer

def send_ticket_email(email, ticket_id, pdf_buffer, day):

    msg = Message(
        subject="Tu entrada - Telonautas",
        sender="telonautasteatro@gmail.com",
        recipients=[email],
    )

    dates = {1: "29 de Mayo", 2: "30 de Mayo"}
    hours = {1: "19:00", 2: "18:30"}
    gate_hours = {1: "18:30", 2: "18:00"}
    date_str = dates.get(int(day), f"Día {day}")
    hours_str = hours.get(int(day), f"")
    gate_hours_str = gate_hours.get(int(day), f"")

    msg.body = f"""¡Hola! 👋

Gracias por reservar tu invitación para `Memorias de una bruja mala', el musical que cuenta la verdadera historia de la malvada bruja de Oz. Las entradas no están numeradas.

Nosotros somos Telonautas, una Asociación Cultural sin Ánimo de Lucro con muchas ganas de hacer teatro pero que no cuenta con ningún apoyo. 

Si deseas apoyarnos, aceptaremos donaciones voluntarias en efectivo en una hucha que pondremos tras la función 🙏, ¡para que lo tengas en cuenta! Cualquier ayuda nos hará seguir disfrutando y hacer disfrutar del teatro 🎭❤️ 


📅 {date_str} - {hours_str} h
📍 Caja Blanca, Málaga
🚪 Puertas: {gate_hours_str} h

Tu entrada está adjunta en este mail. Muestra el código en la puerta para que te lo escaneen (impresa o desde el móvil). Si al final no puedes asistir, comunicalo en este mismo mail.

¡Gracias por venir!

---
@telonautasteatro
telonautasteatro@gmail.com
"""

    msg.attach(
            filename = "entrada.pdf",
            content_type = "application/pdf",
            data = pdf_buffer.read()
            )

    mail.send(msg)
