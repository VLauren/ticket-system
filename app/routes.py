from flask import Blueprint, render_template, request, redirect, url_for
from .utils import generate_ticket_id, generate_qr_code, send_ticket_email, generate_ticket_pdf
from .models import email_has_ticket_for_day, save_ticket, get_ticket, mark_ticket_as_used, \
        get_all_tickets, delete_ticket, count_tickets_for_email, tickets_available_for_day
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
    names = request.form.getlist('names')
    email = request.form['email']
    day = request.form['day']
    quantity = len(names)
    
    existing_count = count_tickets_for_email(email, day)
    remaining = 4 - existing_count

    if remaining <= 0:
        return render_template("index.html", error="Ya tienes 4 entradas para este día.")
    if quantity > remaining:
        return render_template("index.html", error=f"Solo puedes reservar {remaining} entrada(s) más para ese día con ese correo.")

    if not tickets_available_for_day(day):
        return render_template("index.html", error="Entradas agotadas para ese día")
    
    # Generate tickets
    tickets = []
    for name in names:
        ticket_id = generate_ticket_id()
        save_ticket(ticket_id, name, email, day)
        generate_qr_code(ticket_id)
        tickets.append({'id': ticket_id, 'name': name})
    
    # Generate PDF
    pdf_buffer = generate_ticket_pdf(tickets, day)
    
    # Send email with PDF
    send_ticket_email(email, tickets, pdf_buffer, day)

    return render_template("success.html")

@main.route('/success')
def success():
    return render_template("success.html")

@main.route('/scan1')
@require_auth
def scan1():
    return render_template("scan.html", day=1)

@main.route('/scan2')
@require_auth
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
@require_auth
def admin_tickets():
    tickets = get_all_tickets()
    day1count = sum(1 for t in tickets if int(t['day']) == 1)
    day2count = sum(1 for t in tickets if int(t['day']) == 2)
    return render_template("admin_tickets.html", tickets=tickets, day1count=day1count, day2count=day2count)

@main.route('/admin/tickets/<ticket_id>/delete', methods=['POST'])
def delete_ticket_route(ticket_id):
    delete_ticket(ticket_id)
    return redirect(url_for('main.admin_tickets'))

@main.route('/privacidad')
def privacidad():
    return render_template("privacidad.html")
