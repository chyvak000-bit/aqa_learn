from sqlalchemy import select
from sqlalchemy.orm import Session

from main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        statement = select(Credit).where(
            Credit.account_id == account_id
        )
        return db.scalar(statement)
