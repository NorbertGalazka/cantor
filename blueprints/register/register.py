from flask import flash, Blueprint, request, session, render_template, redirect, url_for
from user_pass import UserLog


register_blueprint = Blueprint("register", __name__, template_folder='templates')


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register_route():
    actual_user = UserLog(session.get('user'))
    actual_user.get_user_info()
    if request.method == 'GET':
        return render_template('register.html', active_menu='register', actual_user=actual_user)
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if len(password) < 4:
            flash('password cannot be less than 4 characters long')
            return render_template('register.html', active_menu='register',
                                   username=username, actual_user=actual_user, email=email)
        log = UserLog(username, password, email)
        register_data_available = log.register()
        if register_data_available:
            flash('You are registered correctly!')
            return redirect(url_for('index.index'))
        else:
            return redirect(url_for('register.register_route'))



