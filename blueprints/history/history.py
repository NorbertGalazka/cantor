from flask import render_template, Blueprint
from database_connect import get_db


history_blueprint = Blueprint("history", __name__, template_folder='templates')


@history_blueprint.route('/history')
def history():
    db = get_db()
    sql_command = """select id, currency, amount, trans_date from transactions;"""
    cur = db.execute(sql_command)
    transactions = cur.fetchall()
    return render_template('history.html', transactions=transactions, active_menu='history')
