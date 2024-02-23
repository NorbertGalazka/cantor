from flask import Blueprint, redirect, url_for
from database_connect import get_db


delete_transaction_blueprint = Blueprint("delete_transaction", __name__, template_folder='templates')


@delete_transaction_blueprint.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    db = get_db()
    sql_statement = '''delete from transactions where id = ?;'''
    db.execute(sql_statement, [transaction_id])
    db.commit()

    return redirect(url_for('history.history'))