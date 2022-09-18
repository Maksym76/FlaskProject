from celery import Celery
from datetime import datetime
import models
import database

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task
def task1(user_id, currency_UPS1, currency_UPS2, amount1, transaction_id):
    date = datetime.now().strftime('%d.%m.%Y: %X')
    database.init_db()
    transaction_record = models.TransactionQueue.query.filter_by(transaction_id=transaction_id).first()

    user_balance1 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_UPS1).first()
    user_balance2 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_UPS2).first()

    act_currency1 = models.Currency.query.filter_by(currency_name=currency_UPS1).order_by(
        models.Currency.date.desc()).first()
    cur1_cost_to_one_usd = act_currency1.cost_to_one_usd

    act_currency2 = models.Currency.query.filter_by(currency_name=currency_UPS2).order_by(
        models.Currency.date.desc()).first()
    cur2_cost_to_one_usd = act_currency2.cost_to_one_usd

    need_cur2 = amount1 * cur1_cost_to_one_usd / cur2_cost_to_one_usd

    exists_amount_currency2 = act_currency2.available_quantity

    if (user_balance1.balance >= amount1) and (exists_amount_currency2 > need_cur2):
        upgrade_amount_exchanger1 = models.Currency.query.filter_by(date=act_currency1.date,
                                                                    currency_name=currency_UPS1).first()
        upgrade_amount_exchanger1.available_quantity = act_currency1.available_quantity + amount1

        upgrade_amount_exchanger2 = models.Currency.query.filter_by(date=act_currency2.date,
                                                                    currency_name=currency_UPS2).first()
        upgrade_amount_exchanger2.available_quantity = exists_amount_currency2 - need_cur2

        upgrade_user_balance1 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_UPS1).first()
        upgrade_user_balance1.balance = user_balance1.balance - amount1

        upgrade_user_balance2 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_UPS2).first()
        upgrade_user_balance2.balance = user_balance2.balance + need_cur2

        transaction_obj = models.Transaction_history(user_id=user_id, type_of_transaction='exchange',
                                                     amount_of_currency=amount1,
                                                     currency_with_which_the_transaction=currency_UPS1,
                                                     currency_in_which_the_transaction=currency_UPS2,
                                                     data_time=date, amount_of_currency_received=need_cur2,
                                                     commission=0,
                                                     account_id_from_which_the_transaction=user_balance1.id,
                                                     account_id_on_which_the_transaction=user_balance2.id)

        try:

            database.db_session.add(transaction_obj)
            transaction_record.status = 'done'
            database.db_session.add(transaction_record)
            database.db_session.commit()

        except Exception as er:

            return f"{er}"

        return 'Done'

    else:

        transaction_record.status = 'error'
        database.db_session.add(transaction_record)
        database.db_session.commit()

        return "Error"
