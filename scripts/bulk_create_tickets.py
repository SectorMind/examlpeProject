# scripts/bulk_create_tickets.py
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/v1/tickets/"


def generate_tickets(num_rows: int, seats_per_row: int):
    tickets = []
    for row in range(num_rows + 1):
        if row == 0:
            for seat in range(1, 9 + 1):
                if 1 <= seat <= 4 or 11 <= seat <= 16:
                    category_id = 1
                elif 5 <= seat <= 10:
                    category_id = 2
                else:
                    continue  # In case there's an unexpected seat number
        for seat in range(1, seats_per_row + 1):
            if 1 <= seat <= 4 or 11 <= seat <= 16:
                category_id = 1
            elif 5 <= seat <= 10:
                category_id = 2
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


num_rows = 5  # Example: number of rows
seats_per_row = 16  # Example: seats per row

tickets = generate_tickets(num_rows, seats_per_row)

data = {"tickets": tickets}

# response = requests.post(API_URL, json=data)
#
# if response.status_code == 200:
#     print("Tickets created successfully")
# else:
#     print(f"Failed to create tickets: {response.text}")


if __name__ == '__main__':
    print(generate_tickets(5, 16))
