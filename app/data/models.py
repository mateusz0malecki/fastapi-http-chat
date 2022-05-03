import uuid
from .database import Base
from sqlalchemy import String, Text, Column
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(25), unique=True)
    password = Column(Text)

    @staticmethod
    def get_all_users(db):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db, user_id):
        return db.query(User).filter(User.user_id == user_id)

    @staticmethod
    def get_user_by_name(db, user_name):
        return db.query(User).filter(User.username == user_name)

    @staticmethod
    def check_if_user_exists(db, user_name):
        if db.query(User).filter(User.username == user_name).first():
            return True
