from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from data.pika_client import PikaClient
from data.database import get_db
from data import schemas, models
from routes.auth import get_current_user

router = APIRouter(prefix="/messages", tags=["Messages"])

pika_client = PikaClient(host="rabbitmqhost")


@router.get("/{user_name}/{sender}", status_code=status.HTTP_200_OK)
async def get_message(
    sender: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not pika_client.connection or pika_client.connection.is_closed:
        pika_client.setup()
    if not models.User.check_if_user_exists(db, current_user.username):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.username} not found.",
        )
    if not models.User.check_if_user_exists(db, sender):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {sender} not found."
        )
    pika_client.receive_msg(queue_name=f"{sender}.{current_user.username}")
    return pika_client.msg_list


@router.post("/{user_name}", status_code=status.HTTP_201_CREATED)
async def send_message(
    request: schemas.SendMessage,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not pika_client.connection or pika_client.connection.is_closed:
        pika_client.setup()
    if not models.User.check_if_user_exists(db, current_user.username):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.username} not found.",
        )
    if not models.User.check_if_user_exists(db, request.user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {request.user} not found.",
        )
    message = {
        "user_name": current_user.username,
        "message": {"user": request.user, "message": request.message},
    }
    pika_client.publish_msg(message=message)
    return message
