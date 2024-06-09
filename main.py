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
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)


@app.route("/remTask", methods=['POST'])
def remTasks():
    if request.method == "POST":
        user_id = session['user_id']
        task_id = request.json['taskId']

        task = Tasks.query.filter_by(id=task_id).filter_by(user_id=user_id).first()


        try:
            if task:
                db.session.delete(task)
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Задача не найдена. Тех-поддержка: ober1.st8@mail.ru'})
        except Exception as ex:
            return jsonify({'success': False, 'message': ex})
    return jsonify({'success': False, 'message': 'Ошибка доступа. Тех-поддержка: ober1.st8@mail.ru'})


@app.route("/do", methods=["POST"])
def do():
    if request.method == "POST":
        user_id = session['user_id']
        task_id = request.json['taskId']
        status = request.json['status']

        task = Tasks.query.filter_by(id=task_id).filter_by(user_id=user_id).first()
        if task:
            task.status = status
            db.session.commit()
            return jsonify({'success': True, 'status': status})
        else:
            return jsonify({'success': False, 'message':'Задача не найдена. Тех-поддержка: ober1.st8@mail.ru'})
    return jsonify({'success': False, 'message':'Ошибка доступа. Тех-поддержка: ober1.st8@mail.ru'})
@app.route('/newtask', methods=['POST'])
def newtask():
    if request.method == 'POST':
        title = request.json['text']
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            return redirect('/')
        try:
            task = Tasks(title=title, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': False,'error': 'Ошибка доступа.'})
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
    try:
        tasks = Tasks.query.filter_by(user_id=session['user_id']).all()
        return render_template('home.html', tasks=tasks)
    except Exception as e:
        print(e)
        return ''

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
