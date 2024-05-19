from blueprints.register.register import *
import pytest


@pytest.mark.parametrize("email", [
    'norbi.galaz@onet.pl',
    'jan.kowalski@example.com',
    'anna_nowak@gmail.com',
    'jessy_luther@domain.com',
    'sarah.smith85@domain.com',
    'sales@domain.com',
    'abc-d@mail.com'])
def test_valid_email(email):
    assert is_valid_email(email)


@pytest.mark.parametrize("email", [
    'norbi.galaz@onet.pl..',
    'jan.kowalski@example.example.!example.com',
    'anna_nowak@gmail.com//',
    'jess...y_luther@domain..com',
    'sarah.smith85@domain.com;',
    'sales@domain.com..',
    'abc-d@mail.com..'])
def test_invalid_email(email):
    assert is_valid_email(email) is None



# class Twitter:
#     def __init__(self, backend=None, tweets=None):
#         self.backend = backend
#         self.tweets = None
#
#
# @pytest.fixture(params=[None, 'test.txt'])
# def twitter(request):
#     backend_param, tweets_param = request.param
#     twitter = Twitter(backend=backend_param, tweets=tweets_param)
#     yield twitter
