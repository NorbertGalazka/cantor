from flask import request, render_template, flash, Blueprint, session, redirect, url_for
from extensions import db
from user_pass import UserLog, Transaction
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField
from wtforms.validators import DataRequired, ValidationError
import requests
import json
import codecs


exchange_blueprint = Blueprint("exchange", __name__, template_folder='templates')


class ExchangeForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ExchangeForm, self).__init__(*args, **kwargs)
        self.cantor_offer = CantorOffer()  # Inicjalizacja obiektu CantorOffer
        self.cantor_offer.load_currencies()  # Wczytanie dostępnych walut

        # Dynamiczne generowanie listy opcji dla pola wyboru currency
        self.currency.choices = [(currency.code, currency.name) for currency in self.cantor_offer.get_currencies()]
        self.other_currency.choices = [(currency.code, currency.name) for currency in self.cantor_offer.get_currencies()]

    def validate_non_negative(self, field):
        if field.data < 0:
            raise ValidationError('Amount must be non-negative.')

    def validate_currency(self, field):
        # Sprawdzenie czy wybrana waluta istnieje w dostępnych walutach
        currency_code = field.data
        if currency_code not in [currency.code for currency in self.cantor_offer.get_currencies()]:
            raise ValidationError('Invalid currency selected.')

    def validate_other_currency(self, field):
        # Sprawdzenie czy wybrana waluta other_currency jest jedną z dostępnych walut
        other_currency_code = field.data
        if other_currency_code not in [currency.code for currency in self.cantor_offer.get_currencies()]:
            raise ValidationError('Invalid other currency selected.')

    amount = DecimalField('Amount', validators=[DataRequired('Enter amount'), validate_non_negative])
    currency = SelectField('Currency', validators=[DataRequired('Select currency'), validate_currency])
    other_currency = SelectField('Other Currency', validators=[DataRequired('Select other currency'), validate_other_currency])


class CurrencyConverter:
    def __init__(self, currency_code: str, amount, second_currency_code: str):
        self.currency_code = currency_code.upper()
        self.amount = amount
        self.second_currency_code = second_currency_code.upper()

    def get_currency_value_in_pln(self, code: str) -> float:
        if code == 'PLN':
            return 1.0

        try:
            response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/a/{code}/?format=json')
            response.raise_for_status()  # To podniesie wyjątek HTTPError jeśli status jest 4xx lub 5xx
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Błąd podczas pobierania danych dla {code}: {e}")

        try:
            decoded_data = codecs.decode(response.text.encode(), 'utf-8-sig')
            response_data = json.loads(decoded_data)
            return float(response_data['rates'][0]['mid'])
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Błąd podczas przetwarzania danych dla {code}: {e}")

    def get_value(self):
        value_in_pln = self.get_currency_value_in_pln(self.currency_code)
        second_currency_value_in_pln = self.get_currency_value_in_pln(self.second_currency_code)
        return value_in_pln / second_currency_value_in_pln * self.amount


class Currency:
    def __init__(self, code: str, name: str, img_path: str):
        if len(code) == 3:
            self.code = code
        else:
            raise Exception("Currency code must have 3 characters!")
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

    def get_currencies(self):
        return self.currencies

    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return None


@exchange_blueprint.route('/exchange', methods=["GET", "POST"])
def exchange():
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    if not actual_user.is_active:
        return redirect(url_for('login.login'))

    offer = CantorOffer()
    offer.load_currencies()

    form = ExchangeForm()

    if form.validate_on_submit():
        currency = form.currency.data
        other_currency = request.form['other_currency']
        amount = form.amount.data

        try:
            convert = CurrencyConverter(currency_code=currency, amount=float(amount),
                                        second_currency_code=other_currency)
            value = convert.get_value()
            quantity_received = round(value, 2)

            db.session.add(Transaction(currency=currency, amount=float(amount), other_currency=other_currency,
                                       quantity_received=quantity_received, user_name=actual_user.username))
            db.session.commit()

            return render_template('exchange_results.html',
                                   currency=currency, amount=amount,
                                   other=other_currency, currency_info=offer.get_by_code(currency),
                                   quantity_received=quantity_received, value=value, active_menu='exchange',
                                   actual_user=actual_user)
        except ValueError as e:
            flash(f'Wystąpił błąd: {e}', 'error')
            return redirect(url_for('exchange.exchange'))
    else:
        # Debugging information
        print("Form validation failed")
        print(form.errors)

    return render_template('exchange.html', active_menu='exchange',
                           offer=offer, actual_user=actual_user, form=form)
