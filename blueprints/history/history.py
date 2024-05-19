from flask import render_template, Blueprint, session, redirect, url_for
from database_connect import get_db
from user_pass import UserLog, Transaction
from extensions import db

history_blueprint = Blueprint("history", __name__, template_folder='templates')


@history_blueprint.route('/history')
def history():
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    if not actual_user.is_active:
        return redirect(url_for('login.login'))

    transactions = Transaction.query.filter(Transaction.user_name == actual_user.username).all()
    return render_template('history.html', transactions=transactions, active_menu='history',
                           actual_user=actual_user)
