from decimal import Decimal

import requests

from robokassa import generate_payment_link, result_payment, check_success_payment, calculate_signature
import os
from app.config import SHOPID, PASSWORD1, PASSWORD2
from app.exeptions import BaseException


def generate_post_info(
        out_sum: int | float,
        merchant_login: str,
        description: str,
        signature_value: str,
        inv_id=0
):
    if len(description) > 100:
        description = description[:100]
    try:
        int(signature_value, base=16)
    except ValueError as err:
        # print(err)
        raise BaseException(f"signature_value 'f{signature_value}' is not correct")
    out_sum = Decimal(out_sum)
    return f'MerchantLogin={merchant_login}&OutSum={out_sum}&invoiceID=&Receipt=%257B%2522items%2522%253A%255B%257B%2522name%2522%253A%2522%25D0%25A2%25D0%25B5%25D1%2585%25D0%25BD%25D0%25B8%25D1%2587%25D0%25B5%25D1%2581%25D0%25BA%25D0%25B0%25D1%258F%2B%25D0%25B4%25D0%25BE%25D0%25BA%25D1%2583%25D0%25BC%25D0%25B5%25D0%25BD%25D1%2582%25D0%25B0%25D1%2586%25D0%25B8%25D1%258F%2B%25D0%25BF%25D0%25BE%2BRobokassa%2522%252C%2522quantity%2522%253A1%252C%2522sum%2522%253A1%252C%2522tax%2522%253A%2522none%2522%257D%255D%257D&SignatureValue=43d63dca478b2d5a346bb64d0135aee7'


if __name__ == '__main__':
    print(SHOPID)
    out_sum = 100
    sign_value = calculate_signature(SHOPID, out_sum, PASSWORD1)
    print(sign_value)
    print(int(sign_value, base=16))
    try:
        generate_post_info(out_sum=out_sum, merchant_login=SHOPID, description="description",
                           signature_value=sign_value)
    except BaseException as e:
        print(e)
    payload = {
        "MerchantLogin": str(SHOPID),
        "OutSum": 100,
        "invoiceID": "",
        "Receipt": "description",
        "SignatureValue": sign_value,
        # "IsTest": 1
    }
    response = requests.post("https://auth.robokassa.ru/Merchant/Indexjson.aspx?", data=payload)
    print(response.text)
