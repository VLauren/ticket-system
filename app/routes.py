from flask import Blueprint, render_template, request, redirect, url_for
from .utils import generate_ticket_id, generate_qr_code, send_ticket_email
from .models import save_ticket

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    email = request.form['email']
    
    ticket_id = generate_ticket_id()

    save_ticket(ticket_id, name, email)

    qr_path = generate_qr_code(ticket_id)
    qr_url = url_for('static', filename=f"qrcodes/{ticket_id}.png")

    send_ticket_email(email, ticket_id)

    return render_template("success.html", qr_path=qr_url)
    # return redirect(url_for('main.success'))

@main.route('/success')
def success():
    return render_template('success.html')

