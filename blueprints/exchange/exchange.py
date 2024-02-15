from flask import Flask, request, render_template, flash, Blueprint
import requests
import json
import codecs
import re


exchange_blueprint = Blueprint("exchange", __name__, template_folder='templates')


class CurrencyConverter:
    def __init__(self, currency_code: str, amount, second_currency_code: str):
        self.currency_code = currency_code
        self.amount = amount
        self.second_currency_code = second_currency_code

    def get_currency_value_in_pln(self) -> float:
        if self.currency_code == 'PLN':
            return 1.0
        response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/a/{self.currency_code}/?format=json')
        decoded_data = codecs.decode(response.text.encode(), 'utf-8-sig')
        response = json.loads(decoded_data)
        return float(response['rates'][0]['mid'])

    def get_second_currency_value_in_pln(self) -> float:
        if self.second_currency_code == 'PLN':
            return 1.0
        response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/a/{self.second_currency_code}/?format=json')
        decoded_data = codecs.decode(response.text.encode(), 'utf-8-sig')
        response = json.loads(decoded_data)
        return float(response['rates'][0]['mid'])

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

    def load_currencies(self):
        self.currencies.append(Currency("USD", 'Dolar', 'dollaro.jpg'))
        self.currencies.append(Currency("PLN", 'Złoty', 'zloty.jpg'))
        self.currencies.append(Currency("EUR", 'Euro', 'euro.jpg'))
        self.currencies.append(Currency('CHF', 'Frank', 'euro.jpg'))
        self.currencies.append(Currency('GBP', 'Funt', 'euro.jpg'))

    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return None


@exchange_blueprint.route('/exchange', methods=["GET", "POST"])
def exchange():
    offer = CantorOffer()
    offer.load_currencies()
    if request.method == "GET":
        return render_template('exchange.html', offer=offer)
    else:
        currency = request.form['currency']
        other_currency = request.form['other_currency']
        amount = request.form['amount']
        pattern = r'^[\d,.]+$'
        if re.match(pattern, amount):
            amount = amount.replace(',', '.')
            convert = CurrencyConverter(currency_code=currency, amount=float(amount), second_currency_code=other_currency)
            quantity_received = convert.get_currency_value_in_pln()
            value = round(convert.get_value(), 2)
            print(value)

            return render_template('exchange_results.html',
                                   currency=currency, amount=amount,
                                   other=other_currency, currency_info=offer.get_by_code(currency),
                                   quantity_received=quantity_received, value=value)
        else:
            flash('Panie Kostecki nie ze mną te numery ;) Proszę wpisać jeszcze raz z poprawnymi danymi')
            return render_template('exchange.html', offer=offer)