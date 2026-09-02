from sqlalchemy import select
from sqlalchemy.orm import Session

from main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction | None:
        statement = select(Transaction).where(
            Transaction.id == transaction_id
        )
        return db.scalar(statement)

    @staticmethod
    def get_transfer(db: Session, from_account_id: int, to_account_id: int) -> Transaction | None:
        statement = select(Transaction).where(
            Transaction.from_account_id == from_account_id,
            Transaction.to_account_id == to_account_id,
            Transaction.transaction_type == "transfer"
        )
        return db.scalar(statement)

    @staticmethod
    def get_credit_repayment(db: Session, credit_id: int) -> Transaction | None:
        statement = select(Transaction).where(
            Transaction.credit_id == credit_id,
            Transaction.transaction_type == "credit_repayment"
        )
        return db.scalar(statement)
