from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from data import schemas, models
from data.database import get_db
from data.hash import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    return models.User.get_all_users(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def new_user(request: schemas.NewUser, db: Session = Depends(get_db)):
    created_user = models.User(
        username=request.username, password=hash_password(request.password)
    )
    try:
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
        return created_user
    except IntegrityError as e:
        return {"message": "Given username is already used.", "error": e}


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_to_delete = models.User.get_user_by_id(db, user_id)
    if not user_to_delete.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_id={user_id} not found.",
        )
    user_to_delete.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
