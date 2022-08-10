from flask import Flask

from markupsafe import escape

from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello, world!'


@app.get('/currency/<currency_UPS>')
def currency_list():
    pass


@app.get('/currency/<currency_UPS>')
def currency_rating():
    pass


@app.get('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def course_history(currency_UPS1, currency_UPS2):
    pass


@app.get('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def course_ups1_to_ups2(currency_UPS1, currency_UPS2):
    pass


@app.post('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def exchange(currency_UPS1, currency_UPS2):
    pass


@app.get('/currencies')
def amount_of_currency_available():
    pass


@app.get('/currencies')
def currencies_rating():
    pass


@app.get('/user')
def user_balance():
    pass


@app.post('/user/transfer')
def transfer():
    pass


@app.get('/user/history')
def user_history():
    pass


if __name__ == '__main__':
    app.run()
