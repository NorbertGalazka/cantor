from flask import Flask
from blueprints.delete_transaction.delete_transaction import delete_transaction_blueprint
from blueprints.delete_user.delete_user import delete_user_blueprint
from blueprints.edit_user.edit_user import edit_user_blueprint
from blueprints.user_list.user_list import user_list_blueprint
from blueprints.exchange.exchange import exchange_blueprint
from blueprints.register.register import register_blueprint
from blueprints.history.history import history_blueprint
from blueprints.logout.logout import logout_blueprint
from blueprints.index.index import index_blueprint
from blueprints.login.login import login_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.register_blueprint(delete_transaction_blueprint)
app.register_blueprint(delete_user_blueprint)
app.register_blueprint(user_list_blueprint)
app.register_blueprint(edit_user_blueprint)
app.register_blueprint(exchange_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(history_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)


if __name__ == "__main__":
    app.run()

