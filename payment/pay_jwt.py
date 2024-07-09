import base64
import hashlib
import hmac
import json
import requests

# Sample data for the payload
payload = {
    "MerchantLogin": "robo-demo-test",
    "InvoiceType": "OneTime",
    "Culture": "ru",
    "InvId": 0,
    "OutSum": 1,
    "Description": "as",
    "MerchantComments": "no comment",
    "InvoiceItems": [
        {
            "Name": "Тест1",
            "Quantity": 1,
            "Cost": 0.5,
            "Tax": "vat20",
            "PaymentMethod": "full_payment",
            "PaymentObject": "commodity"
        },
        {
            "Name": "Тест2",
            "Quantity": 1,
            "Cost": 0.5,
            "Tax": "vat0",
            "PaymentMethod": "full_prepayment",
            "PaymentObject": "commodity",
            "NomenclatureCode": "IYVITCUR%XE^$X%C^T&VITC^RX&%ERC^TIRX%&ERCUITRXE&ZX%R^CTIR^XUE%ZN1m9E+1¦?5O?6¦?168"
        }
    ]
}

# 1. Create the JWT Header
header = {
    "typ": "JWT",
    "alg": "MD5"
}
header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')

# 2. Create the JWT Payload
payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')

# 3. Generate the Signature
secret_key = "robo-demo-test:pass1"
message = f"{header_b64}.{payload_b64}"
signature = hmac.new(secret_key.encode(), message.encode(), hashlib.md5).hexdigest()

# 4. Construct the JWT
jwt_token = f"{message}.{signature}"

# 5. Send the POST request
url = "https://services.robokassa.ru/InvoiceServiceWebApi/api/CreateInvoice"
headers = {
    "Content-Type": "application/json"
}
response = requests.post(url, headers=headers, data=json.dumps({"jwt": jwt_token}))

# Print the response from the server
print("Response status code:", response.status_code)
print("Response body:", response.text)
