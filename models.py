from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Text, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    currency_name = db.Column(db.String(35), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'currency_name': self.currency_name
        }

class Currency(db.Model):
    __tablename__ = "currency"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    currency_name = db.Column(db.String, nullable=False)
    cost_to_one_usd = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'currency_name': self.currency_name,
            'cost_to_one_usd': self.cost_to_one_usd,
            'available_quantity': self.available_quantity,
            'date': self.date
        }


class Deposite(db.Model):
    __tablename__ = "deposite"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    opening_date = db.Column(db.Text, nullable=False)
    closing_date = db.Column(db.Text, nullable=False)
    balance = db.Column(db.Numeric, nullable=False)
    interest_rate = db.Column(db.Numeric, nullable=False)
    storage_conditions_which_account_id = db.Column(db.Text, nullable=False)


class Rating(db.Model):
    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    currency_name = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'currency_name': self.currency_name,
            'rating': self.rating,
            'comment': self.comment
        }



class Transaction_history(db.Model):
    __tablename__ = "transaction_history"



    id = db.Column(db.Integer,  primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, foreign_key=True, nullable=False)
    type_of_transaction = db.Column(db.String, nullable=False)
    amount_of_currency = db.Column(db.Numeric, nullable=False)
    currency_with_which_the_transaction = db.Column(db.String, nullable=False)
    currency_in_which_the_transaction = db.Column(db.String, nullable=False)
    data_time = db.Column(db.String, nullable=False)
    amount_of_currency_received = db.Column(db.Numeric, nullable=False)
    commission = db.Column(db.Numeric, nullable=False)
    account_id_from_which_the_transaction = db.Column(db.String, nullable=False)
    account_id_on_which_the_transaction = db.Column(db.String, nullable=False)

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

class User(db.Model):
    __tablename__ = "user"


    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String, unique=True,  nullable=False)
    password = db.Column(db.String,  nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password
        }