from flask import flash, Blueprint, request, session, render_template, redirect, url_for
from blueprints.register.register import UserLog


login_blueprint = Blueprint("login", __name__, template_folder='templates')


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' not in session:
        if request.method == 'GET':
            return render_template('login.html', active_menu='login')
        else:
            user_name = request.form['username']
            user_password = request.form['password']
            log = UserLog(user_name, user_password)
            login_record = log.login()

            if login_record is not None:
                session['user'] = user_name
                flash(f'You are logged as {user_name}')
                return render_template('index.html')
            else:
                flash('Login failed, try again!')
                return render_template('login.html', active_menu='login')
    else:
        return redirect(url_for('index.index'))