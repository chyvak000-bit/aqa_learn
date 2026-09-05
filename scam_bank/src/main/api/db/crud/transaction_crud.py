from sqlalchemy import select
from sqlalchemy.orm import Session

from main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_deposit(db: Session, account_id: int) -> Transaction | None:
        statement = select(Transaction).where(
            Transaction.to_account_id == account_id,
            Transaction.transaction_type == "deposit"
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

    @staticmethod
    def get_deposits_by_account_id(db: Session, account_id: int) -> list[Transaction]:
        statement = select(Transaction).where(
            Transaction.to_account_id == account_id,
            Transaction.transaction_type == "deposit"
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def get_transfers_by_account_id(db: Session, account_id: int) -> list[Transaction]:
        statement = select(Transaction).where(
            (Transaction.from_account_id == account_id) |
            (Transaction.to_account_id == account_id),
            Transaction.transaction_type == "transfer"
        )
        return list(db.scalars(statement).all())
