from flask import Blueprint, render_template, session, request, redirect, flash, url_for
from user_pass import UserLog, User
from extensions import db


edit_user_blueprint = Blueprint("edit_user", __name__, template_folder='templates')


@edit_user_blueprint.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    if actual_user.is_admin:
        user = User.query.filter(User.id == user_id).first()
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
            user_record = User.query.filter(User.id == user_id).first()
            user_record.email = email
            user_record.is_active = is_active
            user_record.is_admin = is_admin
            user_record.name = username
            db.session.commit()

            user = User.query.filter(User.id == user_id).first()

            return render_template('edit_user.html', user=user, actual_user=actual_user)

    else:
        flash('you do not have access to these actions, log in as admin')
        return redirect(url_for('index.index'))
