from flask import Flask, request

from markupsafe import escape

import sqlite3

app = Flask(__name__)

def get_data(querry):
    with sqlite3.connect('db1.db') as conn:
        cursor = conn.execute(querry)
        result = cursor.fetchall()
        return result


@app.get('/currency/<currency_UPS>')
def currency_list(currency_UPS):
    result = get_data(f"SELECT * FROM Currency WHERE currency_name = '{currency_UPS}'")
    return result

@app.get('/currency/<currency_UPS>/rating')
def currency_rating(currency_UPS):
    result = get_data(f"SELECT round(avg(rating), 1) FROM Rating WHERE currency_name = '{currency_UPS}'")
    return result


@app.get('/currencies/rating')
def currencies_rating():
    result = get_data(f"SELECT currency_name, round(avg(rating), 1) as rating FROM Rating GROUP by currency_name")
    return result


@app.get('/currency/trade_graph/<currency_UPS1>/<currency_UPS2>')
def course_history(currency_UPS1, currency_UPS2):
    result = get_data("SELECT * FROM Currency WHERE currency_name = 'uah' or currency_name = 'usd'")
    return result

@app.get('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def course_ups1_to_ups2(currency_UPS1, currency_UPS2):
    result = get_data(f"""SELECT round(
    (SELECT cost_to_one_usd FROM Currency WHERE date = '11-08-2022' and currency_name = '{currency_UPS1}') / 
    (SELECT cost_to_one_usd FROM Currency WHERE date = '11-08-2022' and currency_name = '{currency_UPS2}'), 2)""")
    return result

@app.post('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def exchange(currency_UPS1, currency_UPS2):
    pass


@app.get('/currencies/available')
def amount_of_currency_available():
    result = get_data("SELECT currency_name, available_quantity FROM Currency WHERE date = '11-08-2022'")
    return result

@app.get('/user')
def user_balance():
    result = get_data(f"SELECT balance, currency_name FROM Account WHERE user_id = 2")
    return result


@app.post('/user/transfer')
def transfer():
    pass


@app.get('/user/history')
def user_history():
    result = get_data("""SELECT user_id, type_of_transaction, amount_of_currency, currency_with_which_the_transaction, 
    currency_in_which_the_transaction, data_time, amount_of_currency_received, commission, 
    account_from_which_the_transaction, account_on_which_the_transaction FROM Transaction_history WHERE user_id = 1""")
    return result

if __name__ == '__main__':
    app.run()
