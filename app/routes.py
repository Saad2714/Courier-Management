from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PackageInfo
from flask_login import current_user, login_user
from app.models import User, Pkg
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from is_admin import is_admin
import os

admins = ['sal','tanmay','saad','saiakash']

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Sign In', form=form)
    
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Pkg.query.all()
    return render_template('index.html',title='Home',posts=posts,admin=admins)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Fuck Yeah you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/addpkg', methods=['GET','POST'])
@login_required
def addpkg():
    allowed()
    form = PackageInfo()
    if is_admin(current_user.username):
        pkg = Pkg(package=form.package.data, courier=form.courier.data)
        db.session.add(pkg)
        db.session.commit()
        pkgs = Pkg.query.all()
        return render_template('addpkg.html', form = form, admin = admins,pkgs = pkgs)


def allowed():
    form = PackageInfo()

    if is_admin(current_user.username):
        return render_template('addpkg.html', form=form, admin = admins)
    else:
        flash("You're not Admin")
        return redirect(url_for('index'))
