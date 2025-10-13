from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.models import Post, User
from app.forms import PostForm, RegistrationForm, LoginForm

bp = Blueprint('main', __name__)


from flask import request

@bp.route('/')
def index():
    title = 'Главная'
    page = request.args.get('page', 1, type=int)
    per_page = 5  

    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items

    return render_template('index.html', title=title, posts=posts, pagination=pagination)



@bp.route('/about')
def about():
    return "Это мой первый проект на Flask!"


@bp.route('/add', methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            body=form.body.data,
            author=form.author.data,
            user_id=current_user.id  
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Пост создан', 'success')
        return redirect(url_for("main.index"))
    return render_template("add_post.html", form=form)



# Редактирование поста
@bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        flash('Вы не можете редактировать этот пост', 'danger')
        return redirect(url_for('main.index'))

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.author = form.author.data

        db.session.commit()
        flash('Пост обновлён', 'success')
        return redirect(url_for('main.index'))

    return render_template('edit_post.html', form=form)



@bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id is None or post.user_id != current_user.id:
        flash('Вы не можете удалить этот пост', 'danger')
        return redirect(url_for('main.index'))

    db.session.delete(post)
    db.session.commit()
    flash('Пост удалён', 'success')
    return redirect(url_for('main.index'))

# ---- регистрация ----
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно. Войдите в систему.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# ---- вход ----
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Вы вошли в систему', 'success')
            # если был параметр next, то редирект туда
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('login.html', form=form)

# ---- выход ----
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))
