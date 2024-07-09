import decimal
from robokassa import generate_payment_link, result_payment, check_success_payment
import os
from app.config import SHOPID, PASSWORD1, PASSWORD2

# Example Data
consumer = {
    "name": "Bob",
    "email": "test@test.com"
}
ticket = {
    "row": "2",
    "seat": "15"
}

# Booking details
order_number = 123456
cost = decimal.Decimal('100.00')
description = f'Ticket for {consumer["email"]}, Row: {ticket["row"]}, Seat: {ticket["seat"]}'

# Merchant credentials
merchant_login = SHOPID
merchant_password_1 = PASSWORD1
merchant_password_2 = PASSWORD2

# Generate payment link
payment_link = generate_payment_link(
    merchant_login=merchant_login,
    merchant_password_1=merchant_password_1,
    cost=cost,
    number=order_number,
    description=description
)

print("Payment Link:", payment_link)

# Mock ResultURL request from Robokassa
result_url_request = 'https://my-pay.com/result?OutSum=100.00&InvId=123456&SignatureValue=abcdef123456'

# Verify the payment result
result = result_payment(merchant_password_2, result_url_request)
print("Result URL Verification:", result)

# Mock SuccessURL request from Robokassa
success_url_request = 'https://my-pay.com/success?OutSum=100.00&InvId=123456&SignatureValue=abcdef123456'

# Verify the success payment
success = check_success_payment(merchant_password_1, success_url_request)
print("Success URL Verification:", success)


data = {
    "consumer": {
        "name": "Bob",
        "email": "test@test.com"
    },
    "ticket": {
        "row": "2",
        "seat": "15"
    }
}
print(data.get("consumer").values().mapping.get("name"))
