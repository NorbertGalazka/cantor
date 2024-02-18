from flask import Flask, g
from blueprints.index.index import index_blueprint
from blueprints.exchange.exchange import exchange_blueprint


app_info = {'db_file': '/home/norbert-linux/Flask/data/cantor.db'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.register_blueprint(index_blueprint)
app.register_blueprint(exchange_blueprint)


if __name__ == "__main__":
    app.run()

