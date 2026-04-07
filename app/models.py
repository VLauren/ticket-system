from numpy import empty
import pandas as pd
import os
from datetime import datetime

CSV_FILE = 'data/tickets.csv'
MAX_TICKETS_PER_DAY = 200

def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['id', 'name', 'email', 'used', 'day', 'created_at'])
        df.to_csv(CSV_FILE, index=False)

def save_ticket(ticket_id, name, email, day):
    init_csv()

    new_ticket = {
        'id': ticket_id,
        'name': name,
        'email': email,
        'used': False,
        'day': int(day),
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
        
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([new_ticket])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    return new_ticket

def get_ticket(ticket_id):
    init_csv()
    df = pd.read_csv(CSV_FILE)
    ticket = df[df["id"] == ticket_id]
    if ticket.empty:
        return None
    return ticket.iloc[0].to_dict()

def mark_ticket_as_used(ticket_id):
    df = pd.read_csv(CSV_FILE)
    index = df.index[df["id"] == ticket_id]

    if len(index) == 0:
        return False

    df.loc[index, "used"] = True
    df.to_csv(CSV_FILE, index=False)
    return True

def delete_ticket(ticket_id):
    init_csv()
    df = pd.read_csv(CSV_FILE)
    
    if ticket_id not in df['id'].values:
        return False
    
    df = df[df['id'] != ticket_id]
    df.to_csv(CSV_FILE, index=False)
    return True

def email_has_ticket_for_day(email, day):
    init_csv()
    df = pd.read_csv(CSV_FILE)

    if df.empty:
        return False

    match = df[(df['email'] == email) & (df['day'] == int(day))]
    return not match.empty

def get_all_tickets():
    init_csv()
    df = pd.read_csv(CSV_FILE)

    if df.empty:
        return []

    df = df.sort_values('created_at', ascending=False)

    return df.to_dict('records')

def count_tickets_for_day(day):
    init_csv()
    df = pd.read_csv(CSV_FILE)
    
    if(df.empty):
        return 0

    count = len(df[df['day'] == int(day)])
    return count

def tickets_available_for_day(day):
    return count_tickets_for_day(day) < MAX_TICKETS_PER_DAY

