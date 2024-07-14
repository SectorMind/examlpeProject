# scripts/bulk_create_tickets.py
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/v1/tickets/"


def generate_tickets(num_rows: int, seats_per_row: int):
    tickets = []
    for row in range(num_rows + 1):
        if row == 0:
            for seat in range(1, seats_per_row + 1 - 8):
                if 1 <= seat <= 4 or 11 <= seat <= 14:
                    category_id = 3
                elif 5 <= seat <= 6 or 9 <= seat <= 10:
                    category_id = 2
                elif 7 <= seat <= 8:
                    category_id = 1
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "event_id": 1,
                    "row": str(row),
                    "seat": str(seat),
                    "category_id": category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (1, 2):
            for seat in range(1, seats_per_row + 1 - 2):
                if 1 <= seat <= 5 or 16 <= seat <= 20:
                    category_id = 5
                elif 6 <= seat <= 15:
                    category_id = 4
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "event_id": 1,
                    "row": str(row),
                    "seat": str(seat),
                    "category_id": category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (3, 4, 5, 6):
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 6 or 17 <= seat <= 22:
                    category_id = 7
                elif 7 <= seat <= 16:
                    category_id = 6
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "event_id": 1,
                    "row": str(row),
                    "seat": str(seat),
                    "category_id": category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (7, 8, 9, 10):
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 6 or 17 <= seat <= 22:
                    category_id = 8
                elif 7 <= seat <= 16:
                    category_id = 7
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "event_id": 1,
                    "row": str(row),
                    "seat": str(seat),
                    "category_id": category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)
        if row in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22):
            for seat in range(1, seats_per_row + 1):
                if 1 <= seat <= 22:
                    category_id = 9
                else:
                    continue  # In case there's an unexpected seat number
                ticket = {
                    "event_id": 1,
                    "row": str(row),
                    "seat": str(seat),
                    "category_id": category_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                tickets.append(ticket)

    return tickets


if __name__ == '__main__':
    num_rows = 22  # Example: number of rows
    seats_per_row = 22  # Example: seats per row

    tickets = generate_tickets(num_rows, seats_per_row)
    print(tickets)

    # data = {"tickets": tickets}
    # response = requests.post(API_URL, json=data)
    #
    # if response.status_code == 200:
    #     print("Tickets created successfully")
    # else:
    #     print(f"Failed to create tickets: {response.text}")
