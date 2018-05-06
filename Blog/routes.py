from flask import render_template, url_for, flash, redirect, request
import secrets
import os
from Blog import app, db, bcrypt
from Blog.models import User, Post
from Blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def Main():
    posts= Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def About():
    return render_template('about.html', title= 'About')


@app.route('/register', methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Main'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account Created for {}'.format(form.username.data), 'success')
        return redirect(url_for('Main'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('Main'))
        else:
            flash('Login Unsuccesful', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('Main'))

def save_picture(form_picture):
    random_hex= secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@login_required
@app.route('/account', methods=['GET', 'POST'])
def Account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Username and Password has Been Updated", 'success')
    elif request.method == 'GET':
        form.username.data == current_user.username
        form.email.data == current_user.email
    img_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    return render_template('account.html', title='Account', image_file=img_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def New_Post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('Main'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')
