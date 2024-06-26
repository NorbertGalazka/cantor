from flask import flash, Blueprint, request, session, render_template, redirect, url_for
from user_pass import UserLog
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms import StringField


login_blueprint = Blueprint("login", __name__, template_folder='templates')


class LoginForm(FlaskForm):
    login = StringField('Login')




@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()

    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', active_menu='login', actual_user=actual_user, form=form)
    else:
        user_name = request.form['username']
        user_password = request.form['password']
        user = UserLog(user_name, user_password)
        user_data = user.login()

        if user_data:
            session['user'] = user_data.name
            flash(f'''You are logged as {user_data.name}''')
            return redirect(url_for('index.index'))
        else:
            flash('Login failed, try again!')
            return redirect(url_for('login.login'))


