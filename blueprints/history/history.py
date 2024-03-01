from flask import render_template, Blueprint, session, redirect, url_for
from database_connect import get_db
from user_pass import UserLog


history_blueprint = Blueprint("history", __name__, template_folder='templates')


@history_blueprint.route('/history')
def history():
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    if not actual_user.is_active:
        return redirect(url_for('login.login'))
    db = get_db()
    sql_command = """SELECT id, currency, amount, trans_date from transactions WHERE user=?;"""
    cur = db.execute(sql_command, [actual_user.username])
    transactions = cur.fetchall()
    return render_template('history.html', transactions=transactions, active_menu='history',
                           actual_user=actual_user)
