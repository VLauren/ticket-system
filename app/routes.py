from flask import Blueprint, render_template, request, redirect, url_for
from .utils import generate_ticket_id, generate_qr_code, send_ticket_email, generate_ticket_pdf
from .models import save_ticket, get_ticket, mark_ticket_as_used

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    email = request.form['email']
    day = request.form['day']
    
    ticket_id = generate_ticket_id()

    save_ticket(ticket_id, name, email, day)

    qr_path = generate_qr_code(ticket_id)
    pdf_path = generate_ticket_pdf(ticket_id, name, day)
    qr_url = url_for('static', filename=f"qrcodes/{ticket_id}.png")

    # send_ticket_email(email, ticket_id)
    send_ticket_email(email, ticket_id, pdf_path)

    return render_template("success.html", qr_path=qr_url)
    # return redirect(url_for('main.success'))

@main.route('/success')
def success():
    return render_template("success.html")

@main.route('/scan1')
def scan1():
    return render_template("scan.html", day=1)

@main.route('/scan2')
def scan2():
    return render_template("scan.html", day=2)

@main.route('/ticket/<ticket_id>')
def ticket(ticket_id):
    scan_day = request.args.get('day')

    ticket = get_ticket(ticket_id)
    if ticket is None:
        status = "invalid"
    elif str(ticket["day"]) != str(scan_day):
        status = "wrong_day"
    elif ticket["used"]:
        status = "already_used"
    else:
        mark_ticket_as_used(ticket_id)
        status = "valid"
    return render_template("ticket_status.html", ticket_id=ticket_id, status=status)
    return f"Entrada escaneada: {ticket_id}"

