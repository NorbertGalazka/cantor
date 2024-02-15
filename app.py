from flask import Flask
from blueprints.index.index import index_blueprint
from blueprints.exchange.exchange import exchange_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.register_blueprint(index_blueprint)
app.register_blueprint(exchange_blueprint)


if __name__ == "__main__":
    app.run()

