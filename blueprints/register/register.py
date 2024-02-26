from database_connect import get_db
from flask import flash, Blueprint, request, session, render_template, redirect, url_for


register_blueprint = Blueprint("register", __name__, template_folder='templates')


class UserLog:
    def __init__(self, username, password, *args):
        self.username = username
        self.password = password
        if args:
            self.email = args[0]

    def register(self):
        db = get_db()
        sql_command = f"""SELECT name, email from users WHERE name=='{self.username}' OR email=='{self.email}';"""
        cur = db.execute(sql_command)
        captured_values = cur.fetchall()
        captured_values_list = []
        for value in captured_values:
            if value['email'] == self.email:
                captured_values_list.append(self.email)
                flash(f'Unfortunately email {self.email} is already used')
            if value['name'] == self.username:
                captured_values_list.append(self.username)
                flash(f'Unfortunately username {self.username} is already used')
        if captured_values_list:
            db.close()
            return False
        else:
            try:
                db.execute("""INSERT INTO users(name, email, password, is_active, is_admin)
                                VALUES(?,?,?, True, False);""",
                           [self.username, self.email, self.password])
                db.commit()
            finally:
                db.close()
            return True

    def login(self):
        db = get_db()
        sql_statement = 'select id, name, password, is_active, is_admin from users where name=?'
        cur = db.execute(sql_statement, [self.username])
        user_record = cur.fetchone()
        db.close()

        if user_record is not None and user_record['password'] == self.password:
            return user_record
        else:
            return None


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' not in session:
        if request.method == 'GET':
            return render_template('register.html', active_menu='register')
        else:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            log = UserLog(username, password, email)
            register_data_available = log.register()
            if register_data_available:
                flash('You are registered correctly!')
                return redirect(url_for('index.index'))
            else:
                return redirect(url_for('register'))
    else:
        return redirect(url_for('index.index'))


