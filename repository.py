from models import User, Account
from connection import engine
from sqlalchemy import and_
from sqlalchemy.orm import Session


def create_user(user):
    with Session(autoflush=False, bind=engine) as db:
        db.add(user)
        db.commit()


def get_user_by_id(_id):
    with Session(autoflush=False, bind=engine) as db:
        user = db.query(User).filter(and_(User.id == _id,
                                          User.is_deleted == False)).first()

    return user


def update_user(user_id, _user):
    with Session(autoflush=False, bind=engine) as db:
        db_user = db.query(User).filter(and_(User.id == user_id,
                                        User.is_deleted == False)).first()
        if db_user is not None:
            db_user.name = _user.name
            db_user.surname = _user.surname
            db_user.age = _user.age

            db.commit()


def delete_user(user_id):
    with Session(autoflush=False, bind=engine) as db:
        user = db.query(User).filter(and_(User.id == user_id,
                                          User.is_deleted == False,)).first()
        account = db.query(Account).filter(and_(Account.user_id == user_id,
                                                Account.is_deleted == False)).first()
        if user is not None and account is None:
            user.is_deleted = True
            db.commit()


def create_account(account):
    with Session(autoflush=False, bind=engine) as db:
        db.add(account)
        db.commit()


def get_account_by_user_id(user_id):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Account).filter(and_(Account.user_id == user_id,
                                                Account.is_deleted == False,)).all()

    return account


def delete_account(user_id, account_number):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Account).filter(and_(Account.user_id == user_id,
                                                Account.account_number == account_number,
                                                Account.is_deleted == False)).first()
        if account is not None and account.balance == 0:
            account.is_deleted = True
            db.commit()


def top_up_balance(account_number, new_balance):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Account).filter(and_(Account.account_number == account_number,
                                                Account.is_deleted == False)).first()
        if account is not None:
            account.balance = account.balance + new_balance
            db.commit()


def withdrawing_money(user_id, account_number, new_balance):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Account).filter(and_(Account.user_id == user_id,
                                                Account.account_number == account_number,
                                                Account.is_deleted == False)).first()
        if account is not None and account.balance >= new_balance:
            account.balance = account.balance - new_balance
            db.commit()


def transfer_account(user_id, transfer_account_number, receive_account_number, new_balance):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Account).filter(and_(Account.user_id == user_id,
                                                Account.account_number == transfer_account_number,
                                                Account.is_deleted == False)).first()
        if account is not None and account.balance >= new_balance:
            account.balance = account.balance - new_balance
            receive_account = db.query(Account).filter(and_(Account.account_number == receive_account_number,
                                                            Account.is_deleted == False)).first()

            if receive_account is not None:
                receive_account.balance = receive_account.balance + new_balance
                db.commit()
