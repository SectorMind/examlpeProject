from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ConsumerTicketLink, Consumer, Ticket
from app.database import get_async_session
from app.schemas import PurchasePayload, PaymentRequest

import uuid

from yookassa import Configuration, Payment
from app.config import SHOP_ID_YOOKASSA, SECRET_KEY_YOOKASSA

Configuration.configure(SHOP_ID_YOOKASSA, SECRET_KEY_YOOKASSA)

router = APIRouter()


# @router.post("/payment/")
# async def take_payment_response(consumer: schemas.Consumer, db: AsyncSession = Depends(get_async_session)):
#     # db_consumer = await crud.create_consumer(db=db, consumer=consumer)
#     # if db_consumer is None:
#     #     raise HTTPException(status_code=400, detail="Consumer creation failed")
#     # Grom user data generate link and return it to user
#     generate_payment_link
#     # return {'link': link} # better serialize it
#
#
# @router.get("/payment/")
# async def make_payment(db: AsyncSession = Depends(get_async_session)):
#     """
#         Await for request like 'https://my-pay.com/result?OutSum=100.00&InvId=123456&SignatureValue=abcdef123456'
#         which contains all information about payment:
#         OutSum
#         InvId
#         SignatureValue
#         :param db:
#         :return:
#     """
#     # check_signature_result(out_sum)
#     # TODO add ticket to database if true
#     return answer

@router.post("/create_payment")
async def create_payment(request: PaymentRequest):
    # Generate a unique identifier for the payment
    payment_idempotence_key = str(uuid.uuid4())

    # Create a payment in YooKassa
    payment_data = {
        "amount": {
            "value": str(request.amount),
            "currency": request.currency
        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.return_url
        },
        "description": request.description
    }

    try:
        # Create a payment request
        payment = Payment.create(payment_data, payment_idempotence_key)
        # Return the payment information including the confirmation URL
        return {"id": payment.id, "status": payment.status, "confirmation_url": payment.confirmation.confirmation_url}
    except Exception as e:
        return {"error": str(e)}
