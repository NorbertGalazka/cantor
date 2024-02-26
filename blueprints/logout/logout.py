from flask import flash, Blueprint, session, redirect, url_for


logout_blueprint = Blueprint("logout", __name__, template_folder='templates')


@logout_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash('You are logged out')
    return redirect(url_for('login'))
