from sqlalchemy import select
from sqlalchemy.orm import Session

from main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return db.scalar(statement)
