from flask import Flask, url_for, render_template, request, redirect, session, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = secrets.token_urlsafe(32)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)


@app.route("/")
def index():
    try:
        if request.cookies.get('auth') == 'True':
            if int(request.cookies.get('user_id')) in [int(i.id) for i in Users.query.all()]:
                session['auth'] = True
                session['user_id'] = request.cookies.get('user_id')
    except:
        pass
    if 'auth' in session and session['auth'] == True:
        return redirect('/home')
    else:
        return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        password_hash = generate_password_hash(password)
        user = Users(username=username, password_hash=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
            session['auth'] = True
            session['user_id'] = user.id
            resp = make_response(jsonify({'success': True}))
            resp.set_cookie('auth', 'True', max_age=60 * 60 * 24 * 7, secure=False, httponly=True)
            resp.set_cookie('user_id', str(user.id), max_age=60 * 60 * 24 * 7, secure=False, httponly=True)
            return resp
        except:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Такой пользователь уже существует'})
    if request.method == 'GET':
        return render_template('login.html')

    return jsonify({'success': False, 'message': 'Ошибка доступа'})


@app.route("/unlogin")
def unlogin():
    if 'auth' in session:
        session['auth'] = False
        session['user_id'] = ''
        resp = make_response(redirect('/'))
        resp.set_cookie('auth', 'false', max_age=60 * 60 * 24 * 7, secure=False, httponly=True)
        resp.set_cookie('user_id', str(' '), max_age=60 * 60 * 24 * 7, secure=False, httponly=True)
        return resp




@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        user = Users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password_hash, password):
                session['auth'] = True
                session['user_id'] = user.id
                resp = make_response(({'success': True}))
                resp.set_cookie('auth', 'True', max_age=60 * 60 * 24 * 7, secure=False, httponly=True)
                resp.set_cookie('user_id', str(user.id), max_age=60 * 60 * 24 * 7, secure=False, httponly=True)
                return resp
            else:
                return jsonify({'success': False, 'message': 'Неверный пароль'})
        return jsonify({'success': False, 'message': 'Пользователя не существует'})
    elif request.method == 'GET':
        return render_template('auth.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
