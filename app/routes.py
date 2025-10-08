from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.models import Post

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    title = 'Главная'
    posts = Post.query.all()
    return render_template('index.html', title=title, posts=posts)


@bp.route('/about')
def about():
    return "Это мой первый проект на Flask!"


@bp.route('/add', methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        author = request.form['author']

        new_post = Post(title=title, body=body, author=author)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("main.index"))
    return render_template("add_post.html")


# Редактирование поста
@bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)  # если пост не найден → 404

    if request.method == 'POST':
        post.title = request.form['title']
        post.body = request.form['body']
        post.author = request.form['author']

        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit_post.html', post=post)


@bp.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))
