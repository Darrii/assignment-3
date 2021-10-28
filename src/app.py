from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(50), nullable = False)
    passw = db.Column(db.String(50), nullable = False)
    token = db.Column(db.String(120), nullable = False)

    def __repr__(self):
        return self.token

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        _login = request.form['login']
        _passw = request.form['passw']
        correctToken = str(User.query.filter_by(login = _login).first())
        data = _login + _passw
        if correctToken == md5(data.encode('utf-8')).hexdigest():
            return '<b>Token: </b>' + correctToken
        else:
            return 'Could not found a user with login: ' + _login
    else:
        return '''<form action="" method="post">
        <p><label for="login">Login: </label>
        <input type="text" id="login" name="login"></p>
        <p><label for="passw">Password: </label>
        <input type="password" id="passw" name="passw"></p>
        <p><input type="submit" value="Enter"></p>
        </form>'''


@app.route('/protected', methods = ['GET'])
def protected():
    if request.method == 'GET':
        _token = request.args.get('token')
        correctToken = str(User.query.filter_by(token = _token).first())
        if (correctToken == _token):
            return '<h1>Hello, token which is provided is correct</h1>'
        else:
            return '<h1>Hello, Could not verify the token</h1>'

if __name__ == '__main__':
    app.run(debug = True) 