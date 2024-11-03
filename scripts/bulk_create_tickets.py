# scripts/bulk_create_tickets.py
import requests
from datetime import datetime

API_URL = "http://localhost:8000/api/v1/tickets/"


def generate_tickets(num_rows: int, seats_per_row: int, event_id: int):
    tickets = []
    for row in range(num_rows + 1):
        if row == 1:
            for seat in range(1, seats_per_row + 1 - 2):
                if 1 <= seat <= 4 or 9 <= seat <= 12:
                    event_category_id = 11
                # elif 5 <= seat <= 6 or 9 <= seat <= 10:
                #     category_id = 2
                elif 5 <= seat <= 8:
                    event_category_id = 10
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "row": str(row),
                    "seat": str(seat),
                    "event_category_id": event_category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row == 2:
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 3 or 12 <= seat <= 14:
                    event_category_id = 13
                elif 4 <= seat <= 11:
                    event_category_id = 12
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "row": str(row),
                    "seat": str(seat),
                    "event_category_id": event_category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (3, 4):
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 3 or 12 <= seat <= 14:
                    event_category_id = 14
                elif 4 <= seat <= 11:
                    event_category_id = 13
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "row": str(row),
                    "seat": str(seat),
                    "event_category_id": event_category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (5, 6):
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 3 or 12 <= seat <= 14:
                    event_category_id = 16
                elif 4 <= seat <= 11:
                    event_category_id = 6
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "row": str(row),
                    "seat": str(seat),
                    "event_category_id": event_category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (7, 8, 9):
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 14:
                    event_category_id = 17
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "row": str(row),
                    "seat": str(seat),
                    "event_category_id": event_category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (10, 11, 12, 13, 14, 15, 16, 17, 18, 19):
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 14:
                    event_category_id = 18
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "row": str(row),
                    "seat": str(seat),
                    "event_category_id": event_category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)

    return tickets


if __name__ == '__main__':
    # num_rows = 22  # Example: number of rows
    # seats_per_row = 22  # Example: seats per row

    tickets = generate_tickets(num_rows=19, seats_per_row=14, event_id=2)
    print(tickets)

    data = {"tickets": tickets}
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        print("Tickets created successfully")
    else:
        print(f"Failed to create tickets: {response.text}")
