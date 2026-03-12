from flask import Blueprint, render_template, request
from .utils import generate_ticket_id
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

    return f"Entrada reservada para {name}"
