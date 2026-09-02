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
