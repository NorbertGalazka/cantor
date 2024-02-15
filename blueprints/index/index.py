from flask import Flask, request, render_template, flash, Blueprint

index_blueprint = Blueprint("index", __name__, template_folder='templates')


@index_blueprint.route('/')
def index():
    return render_template('index.html')