import ast
import os
import sqlite3
import random
from flask import Flask, request, render_template, redirect, make_response, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import abort
from werkzeug.exceptions import abort
from data import db_session
from data.users import User
from data.students import Students
from data.posts import Posts
from forms.user import RegisterForm
from forms.studentform import StudentForm
from forms.loginform import LoginForm
from forms.postform import PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'soalko_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def plan():
    con = sqlite3.connect("db/duties.db")
    cur = con.cursor()

    cursor = cur.execute('SELECT posts_final FROM order_of_posts')
    current_final_posts = cursor.fetchall()
    posts_final = ast.literal_eval(current_final_posts[0][0])

    cursor = cur.execute('SELECT floor FROM posts')
    floors_posts = cursor.fetchall()
    floors_of_posts = []
    for i in floors_posts:
        if i[0] not in floors_of_posts:
            floors_of_posts.append(i[0])

    cursor = cur.execute('SELECT name FROM posts')
    items_names = cursor.fetchall()
    cursor = cur.execute('SELECT floor, name, am_m, am_f FROM posts')
    posts_x = cursor.fetchall()
    ti = []
    for i in items_names:
        if i[0] not in ti:
            ti.append(i[0])

    return render_template('plan.html', error='', ti=ti, floors_of_posts=floors_of_posts, posts_x=posts_x,
                           posts_final=posts_final)


@app.route('/err')
def plan_err():
    con = sqlite3.connect("db/duties.db")
    cur = con.cursor()

    cursor = cur.execute('SELECT posts_final FROM order_of_posts')
    current_final_posts = cursor.fetchall()
    posts_final = ast.literal_eval(current_final_posts[0][0])

    cursor = cur.execute('SELECT floor FROM posts')
    floors_posts = cursor.fetchall()
    floors_of_posts = []
    for i in floors_posts:
        if i[0] not in floors_of_posts:
            floors_of_posts.append(i[0])

    cursor = cur.execute('SELECT name FROM posts')
    items_names = cursor.fetchall()
    cursor = cur.execute('SELECT floor, name, am_m, am_f FROM posts')
    posts_x = cursor.fetchall()
    ti = []
    for i in items_names:
        if i[0] not in ti:
            ti.append(i[0])

    return render_template('plan.html', error='Ошибка! Количество мест на постах больше, чем количество учеников!',
                           ti=ti, floors_of_posts=floors_of_posts, posts_x=posts_x, posts_final=posts_final)


@app.route('/generate_plan')
@login_required
def gen_plan():
    con = sqlite3.connect("db/duties.db")
    cur = con.cursor()
    cursor = cur.execute('SELECT am_m, am_f FROM posts')
    items_names = cursor.fetchall()
    p_sum = 0
    for i in items_names:
        p_sum += sum(i)
    cursor = cur.execute('SELECT id FROM students '
                         'WHERE gender = "М" AND in_plan = TRUE')
    men = cursor.fetchall()
    cursor = cur.execute('SELECT id FROM students '
                         'WHERE gender = "Ж" AND in_plan = TRUE')
    wom = cursor.fetchall()
    men_list = [i[0] for i in men]
    wom_list = [i[0] for i in wom]
    alist = men_list + wom_list

    if p_sum <= len(alist):
        cursor = cur.execute('SELECT floor FROM posts')
        floors_posts = cursor.fetchall()
        floors_of_posts = []
        for i in floors_posts:
            if i[0] not in floors_of_posts:
                floors_of_posts.append(i[0])

        cursor = cur.execute('SELECT name FROM posts')
        items_names = cursor.fetchall()
        cursor = cur.execute('SELECT floor, name, am_m, am_f FROM posts')
        posts_x = cursor.fetchall()
        ti = []
        for i in items_names:
            if i[0] not in ti:
                ti.append(i[0])

        cursor = cur.execute('SELECT id FROM students '
                             'WHERE gender = "М" AND in_plan = TRUE')
        men = cursor.fetchall()
        cursor = cur.execute('SELECT id FROM students '
                             'WHERE gender = "Ж" AND in_plan = TRUE')
        wom = cursor.fetchall()

        men_list = [i[0] for i in men]
        wom_list = [i[0] for i in wom]

        posts_final = []
        for floor_num in floors_of_posts:
            for floor_name in ti:
                for post in posts_x:
                    if post[0] == floor_num and post[1] == floor_name:
                        ml_x, wl_x = [], []
                        ml_temp = random.sample(men_list, post[2])
                        wl_temp = random.sample(wom_list, post[3])
                        men_list = [ele for ele in men_list if ele not in ml_temp]
                        wom_list = [ele for ele in wom_list if ele not in wl_temp]
                        for ml_n in ml_temp:
                            cursor = cur.execute(f'SELECT name, surname FROM students WHERE id = {ml_n}')
                            x = cursor.fetchall()
                            ml_x.append([x[0][0], x[0][1]])
                        for wl_n in wl_temp:
                            cursor = cur.execute(f'SELECT name, surname FROM students WHERE id = {wl_n}')
                            x = cursor.fetchall()
                            wl_x.append([x[0][0], x[0][1]])

                        posts_final.append([ml_x, wl_x, floor_num, floor_name])

        cur.execute(f'REPLACE INTO order_of_posts (id, posts_final) VALUES (1, "{posts_final}")')
        con.commit()
        return redirect('/')

    else:
        return redirect(url_for('plan_err'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(name=form.name.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/students', methods=['GET', 'POST'])
def students():
    con = sqlite3.connect("db/duties.db")
    cur = con.cursor()
    cursor = cur.execute('SELECT id, name, surname, gender, in_plan FROM students')
    items = cursor.fetchall()
    return render_template('students.html', items=items)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    con = sqlite3.connect("db/duties.db")
    cur = con.cursor()
    cursor = cur.execute('SELECT id, name, floor, am_m, am_f FROM posts')
    items = cursor.fetchall()
    return render_template('posts.html', items=items)


@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        std = Students()
        std.name = form.name.data
        std.surname = form.surname.data
        std.gender = form.gender.data
        std.in_plan = form.in_plan.data
        db_sess.add(std)
        db_sess.commit()
        return redirect('/students')
    return render_template('add_student.html', title='Добавление Ученика', form=form)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        pst = Posts()
        pst.name = form.name.data
        pst.floor = form.floor.data
        pst.am_m = form.am_m.data
        pst.am_f = form.am_f.data
        db_sess.add(pst)
        db_sess.commit()
        return redirect('/posts')
    return render_template('add_post.html', title='Добавление Поста', form=form)


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    form = StudentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        std = db_sess.query(Students).filter(Students.id == id).first()
        if std:
            form.name.data = std.name
            form.surname.data = std.surname
            form.gender.data = std.gender
            form.in_plan.data = std.in_plan
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        std = db_sess.query(Students).filter(Students.id == id).first()
        if std:
            std.name = form.name.data
            std.surname = form.surname.data
            std.gender = form.gender.data
            std.in_plan = form.in_plan.data
            db_sess.commit()
            return redirect('/students')
        else:
            abort(404)
    return render_template('add_student.html', title='Редактирование ученика', form=form)


@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = PostForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        pst = db_sess.query(Posts).filter(Posts.id == id).first()
        if pst:
            form.name.data = pst.name
            form.floor.data = pst.floor
            form.am_m.data = pst.am_m
            form.am_f.data = pst.am_f
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        pst = db_sess.query(Posts).filter(Posts.id == id).first()
        if pst:
            pst.name = form.name.data
            pst.floor = form.floor.data
            pst.am_m = form.am_m.data
            pst.am_f = form.am_f.data
            db_sess.commit()
            return redirect('/posts')
        else:
            abort(404)
    return render_template('add_post.html', title='Редактирование поста', form=form)


@app.route('/delete_student/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    db_sess = db_session.create_session()
    std = db_sess.query(Students).filter(Students.id == id).first()
    if std:
        db_sess.delete(std)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/students')


@app.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    db_sess = db_session.create_session()
    pst = db_sess.query(Posts).filter(Posts.id == id).first()
    if pst:
        db_sess.delete(pst)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/posts')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    db_session.global_init("db/duties.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
