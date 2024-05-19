from user_pass import *
import pytest


@pytest.fixture(params=[('norbi','1234', 'test@mail.com'),
                        ('1234', 'qwer', 'mail@com.pl'),
                        ('xdadsad', '1234sa', 'norbert.gala@oney.pl')])
def user_log(request):
    username_param, password_param, mail_param = request.param
    user_log = UserLog(username=username_param, password=password_param, email=mail_param)
    yield user_log


def test_init(user_log):
    assert user_log
