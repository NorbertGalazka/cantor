from database_connect import get_db
from flask import flash
import hashlib
import binascii


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
                                VALUES(?,?,?,?,?);""",
                           [self.username, self.email, self.hash_password(), self.is_active, self.is_admin])
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

        if user_record and self.verify_password(user_record['password'], self.password):
            return user_record
        else:
            return None

    def get_user_info(self):
        db = get_db()
        sql_statement = 'select id, name, password, is_active, email, is_admin from users where name=?'
        cur = db.execute(sql_statement, [self.username])
        db_user = cur.fetchone()

        if db_user is None:
            self.is_active = False
            self.is_admin = False
            self.email = ''
        elif db_user['is_active'] != 1:
            self.is_active = False
            self.is_admin = False
            self.email = db_user['email']
        else:
            self.is_active = True
            self.is_admin = db_user['is_admin']
            self.email = db_user['email']


