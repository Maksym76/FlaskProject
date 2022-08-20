from flask import Flask, request

import sqlite3

from datetime import datetime

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_data(querry):
    with sqlite3.connect('db1.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.execute(querry)
        result = cursor.fetchall()
        conn.commit()
        return result


@app.get('/currency/<currency_UPS>')
def currency_list(currency_UPS):
    result = get_data(f"SELECT * FROM Currency WHERE currency_name = '{currency_UPS}'")
    return {'data': result}


@app.get('/currency/<currency_UPS>/rating')
def currency_rating(currency_UPS):
    result = get_data(f"SELECT round(avg(rating), 1) FROM Rating WHERE currency_name = '{currency_UPS}'")
    return {'data': result}


@app.post('/currency/<currency_UPS>/rating')
def add_currency_rating(currency_UPS):
    request_data = request.get_json()
    comment = request_data['comment']
    rating = request_data['rating']
    get_data(f"INSERT INTO rating (currency_name, rating, comment) VALUES ('{currency_UPS}', '{rating}', '{comment}')")
    return 'ok'


@app.get('/currencies/rating')
def currencies_rating():
    result = get_data(f"SELECT currency_name, round(avg(rating), 1) as rating FROM Rating GROUP by currency_name")
    return {'data': result}


@app.get('/currency/trade_graph/<currency_UPS1>/<currency_UPS2>')
def course_history(currency_UPS1, currency_UPS2):
    result = get_data("SELECT * FROM Currency WHERE currency_name = 'uah' or currency_name = 'usd'")
    return {'data': result}


@app.get('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def course_ups1_to_ups2(currency_UPS1, currency_UPS2):
    result = get_data(f"""SELECT round(
    (SELECT cost_to_one_usd FROM Currency WHERE currency_name = '{currency_UPS1}' ORDER by date DESC LIMIT 1) / 
    (SELECT cost_to_one_usd FROM Currency WHERE currency_name = '{currency_UPS2}' ORDER by date DESC LIMIT 1), 2)
    as exchange_value""")
    return {'data': result}


@app.post('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def exchange(currency_UPS1, currency_UPS2):
    date = datetime.now().strftime('%d.%m.%Y: %X')
    user_id = 1
    amount1 = request.get_json()['amount']

    user_balance1 = get_data(f"SELECT * FROM Account WHERE user_id = '{user_id}' AND currency_name = '{currency_UPS1}'")
    user_balance2 = get_data(f"SELECT * FROM Account WHERE user_id = '{user_id}' AND currency_name = '{currency_UPS2}'")

    act_currency1 = get_data(
        f"""SELECT * FROM Currency WHERE currency_name = '{currency_UPS1}' ORDER by date DESC LIMIT 1""")
    cur1_cost_to_one_usd = act_currency1[0]['cost_to_one_usd']

    act_currency2 = get_data(
        f"""SELECT * FROM Currency WHERE currency_name = '{currency_UPS2}' ORDER by date DESC LIMIT 1""")
    cur2_cost_to_one_usd = act_currency2[0]['cost_to_one_usd']

    need_cur2 = amount1 * cur1_cost_to_one_usd / cur2_cost_to_one_usd

    exists_amount_currency2 = act_currency2[0]['available_quantity']

    if (user_balance1[0]['balance'] >= amount1) and (exists_amount_currency2 > need_cur2):
        get_data(f"""UPDATE Currency SET available_quantity = {act_currency1[0]['available_quantity'] + amount1} 
        WHERE date = '{act_currency1[0]['date']}' AND currency_name = '{currency_UPS1}'""")

        get_data(f"""UPDATE Currency SET available_quantity = {exists_amount_currency2 - need_cur2} 
        WHERE date = '{act_currency2[0]['date']}' AND currency_name = '{currency_UPS2}'""")

        get_data(f"""UPDATE Account SET balance = {user_balance1[0]['balance'] - amount1}  
        WHERE user_id = {user_id} AND currency_name = '{currency_UPS1}'""")

        get_data(f"""UPDATE Account SET balance = {user_balance2[0]['balance'] + need_cur2} 
        WHERE user_id = {user_id} AND currency_name = '{currency_UPS2}'""")

        get_data(f"""INSERT INTO Transaction_history (user_id, type_of_transaction, amount_of_currency, 
        currency_with_which_the_transaction, currency_in_which_the_transaction, data_time, amount_of_currency_received, 
        commission, account_id_from_which_the_transaction, account_id_on_which_the_transaction) VALUES ('{user_id}', 
        'exchange', '{amount1}', '{currency_UPS1}', '{currency_UPS2}', '{date}', {need_cur2}, 0, 
        {user_balance1[0]['id']}, {user_balance2[0]['id']} )""")
        return 'ok'
    else:

        return 'not ok'


@app.get('/currencies/available')
def amount_of_currency_available():
    result = get_data("SELECT currency_name, available_quantity FROM Currency ORDER by date DESC LIMIT 1")
    return {'data': result}


@app.get('/user')
def user_balance():
    result = get_data(f"SELECT balance, currency_name FROM Account WHERE user_id = 2")
    return {'data': result}


@app.post('/user/transfer')
def transfer():
    pass


@app.get('/user/history')
def user_history():
    result = get_data("""SELECT user_id, type_of_transaction, amount_of_currency, currency_with_which_the_transaction, 
    currency_in_which_the_transaction, data_time, amount_of_currency_received, commission, 
    account_from_which_the_transaction, account_on_which_the_transaction FROM Transaction_history WHERE user_id = 1""")
    return {'data': result}


if __name__ == '__main__':
    app.run()
