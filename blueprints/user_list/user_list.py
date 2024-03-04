from flask import Blueprint, render_template, session
from database_connect import get_db
from user_pass import UserLog


user_list_blueprint = Blueprint("user_list", __name__, template_folder='templates')


@user_list_blueprint.route('/user_list')
def user_list():
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    db = get_db()
    sql_command = """SELECT id, name, email, is_active, is_admin from users;"""
    cur = db.execute(sql_command)
    users = cur.fetchall()
    return render_template('user_list.html', users=users, active_menu='users', actual_user=actual_user)
