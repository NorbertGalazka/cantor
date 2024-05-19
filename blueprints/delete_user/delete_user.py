from flask import Blueprint, redirect, url_for
from extensions import db
from user_pass import User


delete_user_blueprint = Blueprint("delete_user", __name__, template_folder='templates')


@delete_user_blueprint.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    db.session.delete(User.query.filter(User.id == user_id).first())
    db.session.commit()

    return redirect(url_for('user_list.user_list'))