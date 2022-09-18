from sqlalchemy import Column, Integer, String, Text, Float, Numeric
from database import Base


class Account(Base):
    __tablename__ = 'account'

    id = Column(Text, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)
    currency_name = Column(String(35), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'currency_name': self.currency_name
        }


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    currency_name = Column(String, nullable=False)
    cost_to_one_usd = Column(Float, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    date = Column(String(12), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'currency_name': self.currency_name,
            'cost_to_one_usd': self.cost_to_one_usd,
            'available_quantity': self.available_quantity,
            'date': self.date
        }


class Deposite(Base):
    __tablename__ = "deposite"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    opening_date = Column(Text, nullable=False)
    closing_date = Column(Text, nullable=False)
    balance = Column(Numeric, nullable=False)
    interest_rate = Column(Numeric, nullable=False)
    storage_conditions_which_account_id = Column(Text, nullable=False)


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    currency_name = Column(String(30), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'currency_name': self.currency_name,
            'rating': self.rating,
            'comment': self.comment
        }


class Transaction_history(Base):
    __tablename__ = "transaction_history"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    type_of_transaction = Column(String, nullable=False)
    amount_of_currency = Column(Numeric, nullable=False)
    currency_with_which_the_transaction = Column(String, nullable=False)
    currency_in_which_the_transaction = Column(String, nullable=False)
    data_time = Column(String, nullable=False)
    amount_of_currency_received = Column(Numeric, nullable=False)
    commission = Column(Numeric, nullable=False)
    account_id_from_which_the_transaction = Column(String, nullable=False)
    account_id_on_which_the_transaction = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type_of_transaction': self.type_of_transaction,
            'amount_of_currency': self.amount_of_currency,
            'currency_with_which_the_transaction': self.currency_with_which_the_transaction,
            'currency_in_which_the_transaction': self.currency_in_which_the_transaction,
            'data_time': self.data_time,
            'amount_of_currency_received': self.amount_of_currency_received,
            'commission': self.commission,
            'account_id_from_which_the_transaction': self.account_id_from_which_the_transaction,
            'account_id_on_which_the_transaction': self.account_id_on_which_the_transaction
        }


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password
        }


class TransactionQueue(Base):
    __tablename__ = "transaction_queue"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    transaction_id = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
