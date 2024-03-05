from flask import Blueprint, render_template, session, request, redirect, flash, url_for
from database_connect import get_db
from user_pass import UserLog


edit_user_blueprint = Blueprint("edit_user", __name__, template_folder='templates')


@edit_user_blueprint.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    if actual_user.is_admin:
        db = get_db()
        sql_statement = '''select * from users where id = ?;'''
        cur = db.execute(sql_statement, [user_id])
        user = cur.fetchone()
        if request.method == 'GET':
            return render_template('edit_user.html', user=user, actual_user=actual_user)
        else:
            email = request.form['email']
            username = request.form['username']
            is_admin = 'gridCheck1' in request.form
            is_active = 'gridCheck2' in request.form
            if is_active:
                is_active = 1
            else:
                is_active = 0
            if is_admin:
                is_admin = 1
            else:
                is_admin = 0

            second_sql_statement = """
                        UPDATE users
                        SET email = ?, is_active = ?, is_admin = ?, name = ?
                        WHERE id = ?;
                        """
            db.execute(second_sql_statement, [email, is_active, is_admin, username, user['id']])
            db.commit()
            sql_statement = '''select * from users where id = ?;'''
            cur = db.execute(sql_statement, [user_id])
            user = cur.fetchone()
            return render_template('edit_user.html', user=user, actual_user=actual_user)

    else:
        flash('you do not have access to these actions, log in as admin')
        return redirect(url_for('index.index'))
