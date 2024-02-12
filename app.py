from flask import Flask, request, render_template, flash
import requests
import json


app = Flask(__name__)


app.config['SECRET_KEY'] = '1234'


class CurrencyConverter:
    def __init__(self, currency_code: str, amount, second_currency: str):
        self.currency_code = currency_code
        self.amount = amount
        self.second_currency = second_currency

    def get_currency_value_in_pln(self) -> float:
        if self.currency_code == 'PLN':
            return 1.0
        response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/a/{self.currency_code}/?format=json')
        response = json.loads(response.text)
        return float(response['rates'][0]['mid'] * self.amount)

    def get_second_currency_value_in_pln(self) -> float:
        if self.currency_code == 'PLN':
            return 1.0
        response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/a/{self.second_currency}/?format=json')
        response = json.loads(response.text)
        return float(response['rates'][0]['mid'] * self.amount)

    def get_value(self):
        return self.get_currency_value_in_pln() / self.get_second_currency_value_in_pln() * self.amount


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
        for currency in [currency, other_currency]:
            if currency in offer.denied_codes:
                flash(f'The currency {currency} cannot be accepted!')

        return render_template('exchange_results.html',
                               currency=currency, amount=amount,
                               other=other_currency, currency_info=offer.get_by_code(currency))


if __name__ == "__main__":
    app.run()

