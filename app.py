from flask import Flask, request, url_for, redirect, render_template, flash
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'


class Currency:
    def __init__(self, code, name, img_path):
        self.code = code
        self.name = name
        self.img_path = img_path


class CantorOffer:
    def __init__(self):
        self.currencies = []
        self.denied_codes = []

    def load_currencies(self):
        self.currencies.append(Currency("USD", 'Dolar', 'dollaro.jpg'))
        self.currencies.append(Currency("PLN", 'Złoty', 'zloty.jpg'))
        self.currencies.append(Currency("EURO", 'Euro', 'euro.jpg'))
        self.currencies.append(Currency('CHF', 'Frank', 'euro.jpg'))
        self.currencies.append(Currency('GBP', 'Funt', 'euro.jpg'))
        self.denied_codes.append("USD")

    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    a = 10
    b = 0
    return f'<h1> We are programmers!: {a / b} </h1>'


@app.route('/cantor/<string:currency>/<int:amount>/<string:other>')
def cantor(currency, amount, other):
    return render_template('cantor.html', currency=currency, amount=amount, other=other)


@app.route('/exchange', methods=["GET", "POST"])
def exchange():
    offer = CantorOffer()
    offer.load_currencies()
    if request.method == "GET":
        return render_template('exchange.html', offer=offer)
    else:
        currency = request.form['currency']
        other_currency = request.form['other_currency']
        amount = request.form['amount']
        if currency in offer.denied_codes:
            flash(f'The currency {currency} cannot be accepted!')
        if other_currency in offer.denied_codes:
            flash(f'The currency {other_currency} cannot be accepted!')

        return render_template('cantor.html',
                               currency=currency, amount=amount,
                               other=other_currency, currency_info=offer.get_by_code(currency))


if __name__ == "__main__":
    app.run()
