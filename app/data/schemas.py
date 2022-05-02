from pydantic import BaseModel


class SendMessage(BaseModel):
    user: str
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserID(BaseModel):
    user_id: int
    username: str
    password: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    username: str

    class Config:
        orm_mode = True


class NewUser(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
