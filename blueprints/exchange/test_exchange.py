from blueprints.exchange.exchange import *
import pytest


@pytest.fixture()
def cantor_offer():
    cantor_offer = CantorOffer()
    return cantor_offer


def test_cantor_offer_init(cantor_offer):
    assert cantor_offer


def test_load_currencies(cantor_offer):
    cantor_offer.load_currencies()
    assert cantor_offer.currencies != []


def test_len_load_currencies(cantor_offer):
    cantor_offer.load_currencies()
    assert len(cantor_offer.currencies) == 5


def test_get_currency_by_code(cantor_offer):
    cantor_offer.load_currencies()
    assert isinstance(cantor_offer.get_by_code('USD'), Currency)


def test_get_currency_by_incorrect_code(cantor_offer):
    cantor_offer.load_currencies()
    assert cantor_offer.get_by_code(2, 2, 'as', True, None) is None


def test_get_currency_by_code_with_wrong_amount_of_arg(cantor_offer):
    cantor_offer.load_currencies()
    assert cantor_offer.get_by_code('PLN', 2, 'as', True, None)


def test_bad_code_currency_append():
    with pytest.raises(Exception):
        bad_currency = Currency('USDA', 'Dolar', 'dollaro.jpg')


@pytest.mark.parametrize('currency', ['USD', 'PLN', 'EUR', 'GBP', 'CHF'])
def test_currency_converter_same_currencies(currency):
    converter = CurrencyConverter(currency, 1, currency)
    assert converter.get_currency_value_in_pln() == converter.get_second_currency_value_in_pln()


def test_get_value_the_same_currencies():
    converter = CurrencyConverter('USD', 12.6, 'USD')
    assert converter.get_value() == converter.amount


def test_amount_correct_values():
    converter = CurrencyConverter('USD', 12.6, 'USD')
    converter2 = CurrencyConverter('USD', 999999, 'USD')
    converter3 = CurrencyConverter('USD', 0.5, 'USD')
    assert converter
    assert converter2
    assert converter3


def test_amount_incorrect_values():
    with pytest.raises(Exception):
        converter = CurrencyConverter('USD', 'str', 'USD')
        assert converter

