from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ConsumerTicketLink, Consumer, Ticket
from app.database import get_async_session
from app.schemas import PurchasePayload


router = APIRouter()


@router.post("/payment/")
async def take_payment_response(consumer: schemas.Consumer, db: AsyncSession = Depends(get_async_session)):
    # db_consumer = await crud.create_consumer(db=db, consumer=consumer)
    # if db_consumer is None:
    #     raise HTTPException(status_code=400, detail="Consumer creation failed")
    # Grom user data generate link and return it to user
    generate_payment_link
    # return {'link': link} # better serialize it


@router.get("/payment/")
async def make_payment(db: AsyncSession = Depends(get_async_session)):
    """
        Await for request like 'https://my-pay.com/result?OutSum=100.00&InvId=123456&SignatureValue=abcdef123456'
        which contains all information about payment:
        OutSum
        InvId
        SignatureValue
        :param db:
        :return:
    """
    # check_signature_result(out_sum)
    # TODO add ticket to database if true
    return answer
