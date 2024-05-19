from flask import Blueprint, redirect, url_for
from extensions import db
from user_pass import Transaction


delete_transaction_blueprint = Blueprint("delete_transaction", __name__, template_folder='templates')


@delete_transaction_blueprint.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    db.session.delete(Transaction.query.filter(Transaction.id == transaction_id).first())
    db.session.commit()

    return redirect(url_for('history.history'))