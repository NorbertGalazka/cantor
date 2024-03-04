from flask import Blueprint, redirect, url_for
from database_connect import get_db


delete_user_blueprint = Blueprint("delete_user", __name__, template_folder='templates')


@delete_user_blueprint.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    db = get_db()
    sql_statement = '''delete from users where id = ?;'''
    db.execute(sql_statement, [user_id])
    db.commit()

    return redirect(url_for('user_list.user_list'))