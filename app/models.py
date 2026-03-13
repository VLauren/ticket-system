import pandas as pd
import os

CSV_FILE = 'tickets.csv'

def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['id', 'name', 'email', 'used'])
        df.to_csv(CSV_FILE, index=False)

def save_ticket(ticket_id, name, email):
    init_csv()

    new_ticket = {
        'id': ticket_id,
        'name': name,
        'email': email,
        'used': False
    }
        
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([new_ticket])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    return new_ticket

def get_ticket(ticket_id)
    init_csv()
    df = pd.read_csv(CSV_FILE)
    ticket = df[df["id"] = ticket_id]
    if ticket.empty:
        return None
    return ticket.iloc[0].to_dict()
