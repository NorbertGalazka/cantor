from flask import render_template, Blueprint, session
from user_pass import UserLog


index_blueprint = Blueprint("index", __name__, template_folder='templates')


@index_blueprint.route('/')
def index():
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    return render_template('index.html', actual_user=actual_user)
