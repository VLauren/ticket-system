from flask import Blueprint, render_template, request, redirect, url_for
from .utils import generate_ticket_id, generate_qr_code, send_ticket_email, generate_ticket_pdf
from .models import email_has_ticket_for_day, save_ticket, get_ticket, mark_ticket_as_used, \
        get_all_tickets, delete_ticket, email_has_ticket_for_day, tickets_available_for_day
from functools import wraps
from flask import request, Response

main = Blueprint('main', __name__)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.password != 'pass':
            return Response(
                    'Acceso denegado',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Contraseña requerida"'}
                )
            return f(*args, **kwargs)
        return decorated

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    email = request.form['email']
    day = request.form['day']
    
    if email_has_ticket_for_day(email, day):
        return render_template("index.html", error="Ya hay una reserva para ese día con este correo.")

    if not tickets_available_for_day(day):
        return render_template("index.html", error="Entradas agotadas para ese día")

    ticket_id = generate_ticket_id()
    save_ticket(ticket_id, name, email, day)

    qr_path = generate_qr_code(ticket_id)
    pdf_buffer = generate_ticket_pdf(ticket_id, name, day)
    qr_url = url_for('static', filename=f"qrcodes/{ticket_id}.png")

    # send_ticket_email(email, ticket_id)
    send_ticket_email(email, ticket_id, pdf_buffer)

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
    return render_template("ticket_status.html", ticket_id=ticket_id, status=status, scan_day=scan_day)
    return f"Entrada escaneada: {ticket_id}"

@main.route('/admin/tickets')
def admin_tickets():
    tickets = get_all_tickets()
    return render_template("admin_tickets.html", tickets=tickets)

@main.route('/admin/tickets/<ticket_id>/delete', methods=['POST'])
def delete_ticket_route(ticket_id):
    delete_ticket(ticket_id)
    return redirect(url_for('main.admin_tickets'))
