from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_PORT'] = '3306'
app.config['MYSQL_DB'] = 'carsharing'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Редирект домой
@app.route('/')
def index():
    return render_template('home.html')

# О нас
@app.route('/about')
def about():
    return render_template('about.html')

# Автомобили
@app.route('/cars')
def cars():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()

    if result > 0:
        return render_template('cars.html', cars=cars)
    else:
        msg = 'Автомобилей нет'
        return render_template('cars.html', msg=msg)

# Данные одного авто
@app.route('/car/<string:id>')
def car(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM cars WHERE id=%s", [id])
    car = cur.fetchone()

    return render_template('car.html', car=car)

class RegisterForm(Form):
    name = StringField('Имя', [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=30)])
    language = StringField('Язык', [validators.DataRequired(), validators.Length(min=2, max=20)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Подтвердите пароль')

# Регистрация нового пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        language = form.language.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users(email, name, lang, pass) VALUES(%s, %s, %s, %s)', (email, name, language, password))
        mysql.connection.commit()
        cur.close()

        flash('Регистрация прошла успешно!', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Вход в личный кабинет
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_user = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute('SELECT * FROM users WHERE email = %s', [email])
        if result > 0:

            data = cur.fetchone()
            password = data['pass']
            name = data['name']

            if sha256_crypt.verify(password_user, password):
                session['logged_in'] = True
                session['email'] = email
                session['name'] = name

                flash('Вход успешно выполнен!', 'success')
                return redirect(url_for('dashboard'))

            else:
                error = 'Неправильный пароль'
                return render_template('login.html', error=error)

        else:
            error = 'Неправильный адрес электронной почты'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Проверка авторизации
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Вы не вошли!', 'danger')
            return redirect(url_for('login'))
    return wrap

# Выход из личного кабинет
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Вы вышли...', 'success')
    return redirect(url_for('login'))

# Отображение личного кабинета
@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', cars=cars)
    else:
        msg = 'Автомобилей нет'
        return render_template('dashboard.html', msg=msg)


# Добавление автомобилей
class RegisterCarsForm(Form):
    model_ru = StringField('Марка(рус)', [validators.DataRequired(), validators.Length(min=3, max=50)])
    model_eng = StringField('Марка(англ)', [validators.DataRequired(), validators.Length(min=3, max=50)])
    c_year = StringField('Год выпуска', [validators.DataRequired(), validators.Length(min=2, max=5)])

# Добавление автомобиля
@app.route('/add_car', methods=['GET', 'POST'])
@is_logged_in
def add_car():
    form = RegisterCarsForm(request.form)
    if request.method == 'POST' and form.validate():
        model_ru = form.model_ru.data
        model_eng = form.model_eng.data
        c_year = form.c_year.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cars(model_ru, model_eng, c_year) VALUES(%s, %s, %s)", (model_ru, model_eng, c_year))

        mysql.connection.commit()
        cur.close()

        send_mail(model_ru, model_eng, c_year)
        flash('Автомобиль добавлен!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_car.html', form=form)

# Редактирование автомобиля
@app.route('/edit_car/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_car(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM cars WHERE id=%s", [id])
    car = cur.fetchone()

    # Используем форму
    form = RegisterCarsForm(request.form)

    # Populate car form fields
    form.model_ru.data = car['model_ru']
    form.model_eng.data = car['model_eng']
    form.c_year.data = car['c_year']

    if request.method == 'POST' and form.validate():
        model_ru = request.form['model_ru']
        model_eng = request.form['model_eng']
        c_year = request.form['c_year']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE cars SET model_ru=%s, model_eng=%s, c_year=%s WHERE id=%s", (model_ru, model_eng, c_year, id))

        mysql.connection.commit()
        cur.close()

        flash('Данные автомобиля обновлены', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_car.html', form=form)

# Удалить автомобиль
@app.route('/delete_car/<string:id>', methods=["POST"])
@is_logged_in
def delete_car(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cars WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash('Машина удалена', 'success')

    return redirect(url_for('dashboard'))

# Отсылка писем при регистрации машины
def send_mail(model_ru, model_eng, c_year):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '690fce4c0a8e05'
    password = 'bfc012ecb54bba'
    message = f"<h3>Вы добавили автомобиль в нашу систему!</h3><ul><li>Марка(ru): {model_ru}" \
              f"</li><li>Марка(eng): {model_eng}</li><li>Год выпуска: {c_year}</li></ul>"

    sender_email = 'carsharing@example.com'
    receiver_email = 'user@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Добавление нового автомобиля на CarSharing'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == '__main__':
    app.secret_key = 'secretkey'
    app.run(debug=True)