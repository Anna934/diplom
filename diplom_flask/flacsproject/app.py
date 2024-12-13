from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/User/PytcharmProjects/diplom_flask/flacsproject/database.db'  # Исправлено: добавлены кавычки
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Добавлено: уникальность
    email = db.Column(db.String(120), unique=True, nullable=False)  # Добавлено: уникальность
    password = db.Column(db.String(80), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        user = User.query.filter_by(username=uname, password=passw).first()
        if user is not None:
            return redirect(url_for("index"))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')  # Добавлено: сообщение об ошибке
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    print(f"Метод: {request.method}")  # Отладочное сообщение
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        confirm_passw = request.form.get('confirm_passw')

        print(f"Полученные данные: {uname}, {mail}, {passw}, {confirm_passw}")  # Отладочное сообщение

        existing_user = User.query.filter_by(username=uname).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует!', 'danger')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=mail).first()
        if existing_email:
            flash('Пользователь с таким email уже существует!', 'danger')
            return redirect(url_for('register'))

        if passw != confirm_passw:
            flash('Пароли не совпадают!', 'danger')
            return redirect(url_for('register'))

        try:
            register = User(username=uname, email=mail, password=passw)
            db.session.add(register)  # Добавляем пользователя в сессию
            db.session.commit()  # Сохраняем данные
            flash('Аккаунт успешно создан!', 'success')
            return redirect(url_for("login"))  # Перенаправляем только после успешного сохранения
        except Exception as e:
            db.session.rollback()  # Откат изменений в случае ошибки
            flash(f'Ошибка при создании аккаунта: {str(e)}', 'danger')

    return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():  # Устанавливаем контекст приложения
        print("Создание базы данных и таблиц...")
        db.create_all()  # Создание базы данных и таблиц
        print("База данных и таблицы созданы.")
    app.run(debug=True)

