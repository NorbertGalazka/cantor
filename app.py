from flask import Flask, request, url_for, redirect, render_template
import os


app = Flask(__name__)

# @app.route('/')
# def index():
#     color = 'green'
#     style = 'italic'
#     if 'color' in request.args:
#         color = request.args['color']
#     if 'style' in request.args:
#         style = request.args['style']
#         print(style)
#     return f'<h1 style="color:{color}; font-style:{style};"> Hello World! </h1>'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    a = 10
    b = 0
    return f'<h1> We are programmers!: {a / b} </h1>'


@app.route('/cantor/<string:currency>/<int:amount>/<string:other>')
def cantor(currency, amount, other):
    return render_template('cantor.html', currency=currency, amount=amount, other=other)


@app.route('/exchange', methods=["GET", "POST"])
def exchange():
    if request.method == "GET":
        return render_template('exchange.html')
    else:
        currency = request.form['currency']
        other_currency = request.form['other_currency']
        amount = request.form['amount']
        return redirect(url_for('cantor', currency=currency, amount=amount, other=other_currency))


@app.route('/cook_form', methods=["GET", "POST"])
def cook_form():
    if request.method == "GET":
        return render_template('cook_form.html')
    else:
        note = request.form['note']
        comment = request.form['comment']
        decision = "Never"
        if 'decision' in request.form:
            decision = "Sure!"
        return render_template('cook_form_result.html', note=note, comment=comment, decision=decision)


if __name__ == "__main__":
    app.run()
