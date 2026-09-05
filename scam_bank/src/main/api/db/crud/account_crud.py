from sqlalchemy import select
from sqlalchemy.orm import Session

from main.api.db.models.account_table import Account


class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        statement = select(Account).where(
            Account.id == account_id
        )
        return db.scalar(statement)

    @staticmethod
    def get_accounts_by_user_id(db: Session, user_id: int) -> list[Account]:
        statement = select(Account).where(
            Account.user_id == user_id
        )
        return list(db.scalars(statement).all())
