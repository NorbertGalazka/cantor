from flask import render_template, Blueprint, session

index_blueprint = Blueprint("index", __name__, template_folder='templates')


@index_blueprint.route('/')
def index():
    if 'user' in session:
        print(session['user'])
    else:
        print('nikt nie zalogowany!')
    return render_template('index.html')