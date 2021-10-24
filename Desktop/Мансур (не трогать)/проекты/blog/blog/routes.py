


from blog import app
from blog.models import db, Post, User, Comment

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from blog.forms import RegForm, PostForm
from werkzeug.utils import secure_filename
import os



@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog_single/<int:post_id>', methods=['GET','POST'])
def blog_single(post_id):
    post = Post.query.get(post_id)
    comments = post.comments
    if request.method == 'POST':
        comment = Comment(name=request.form.get('name'), subject=request.form.get('subject'), 
        email=request.form.get('email'), message=request.form.get('message'),post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Рецепт успешно добавлен!', 'success')
        
    return render_template('blog_single.html', post=post, comments=comments)

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and user.email == request.form.get('email'):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('sign_up.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reg', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('sign_up'))       
    return render_template('reg.html', form=form)


@app.route('/add_post', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        if image:
            file_name = image.filename
            
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            post = Post(title=form.title.data, content=form.content.data, author=current_user, image=file_name)
            db.session.add(post)
            db.session.commit()
            flash('Пост был создан!', 'success')
            return redirect(url_for('index'))
    return render_template('add_post.html', form=form)