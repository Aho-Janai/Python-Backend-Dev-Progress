import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.models import PsStroke


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)


@app.route('/feed')
def feed():
    query = sa.select(PsStroke).order_by(PsStroke.created_at.desc(), PsStroke.id.desc()).limit(50)
    strokes = db.session.scalars(query).all()
    return render_template('feed.html', title='Strokes', strokes=strokes)
