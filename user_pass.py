from datetime import datetime
from flask import flash
import hashlib
import binascii


from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.Text)
    is_active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency = db.Column(db.String(5))
    amount = db.Column(db.Integer)
    trans_date = db.Column(db.Date(), default=datetime.now)
    quantity_received = db.Column(db.Integer)
    other_currency = db.Column(db.String(5))
    user_name = db.Column(db.String, db.ForeignKey('user.name'))


class UserLog:
    def __init__(self, username, password='', email=''):
        self.username = username
        self.password = password
        self.is_admin = 0
        self.is_active = 1
        self.email = email

    def hash_password(self):
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\
        xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    @staticmethod
    def verify_password(stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),
                                      salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def register(self):
        captured_users = User.query.all()
        captured_users_list = []
        for user in captured_users:
            if user.email == self.email:
                captured_users_list.append(self.email)
                flash(f'Unfortunately email {self.email} is already used')
            if user.name == self.username:
                captured_users_list.append(self.username)
                flash(f'Unfortunately username {self.username} is already used')
        if captured_users_list:
            return False
        else:
            new_user = User(name=self.username, email=self.email, password=self.hash_password(), is_active=self.is_active, is_admin=self.is_admin)
            db.session.add(new_user)
            db.session.commit()
            return True

    def login(self):
        user_data = User.query.filter(User.name == self.username).first()

        if user_data and self.verify_password(user_data.password, self.password):
            return user_data
        else:
            return None

    def get_user_info(self):
        db_user = User.query.filter(User.name == self.username).first()

        if db_user is None:
            self.is_active = False
            self.is_admin = False
            self.email = ''
        elif db_user.is_active != 1:
            self.is_active = False
            self.is_admin = False
            self.email = db_user.email
        else:
            self.is_active = True
            self.is_admin = db_user.is_admin
            self.email = db_user.email


