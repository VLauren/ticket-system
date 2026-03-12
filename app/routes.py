from flask import Blueprint, render_template, request
from .utils import generate_ticket_id

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    email = request.form['email']
    
    ticket_id = generate_ticket_id()

    return f"Recibido reserva para {name} con ticket {ticket_id}"
