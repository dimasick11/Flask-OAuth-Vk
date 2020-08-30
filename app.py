from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin

from config import initialization_config
from business_logic import get_concate_username, get_friends_curr_user
from oauth import OAuthSignIn


app = Flask(__name__)
initialization_config(app)

db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = 'index'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(64), nullable = False, unique = True)
    username = db.Column(db.String(128), nullable = False, unique = True)
    token = db.Column(db.String(256), nullable = False, unique = True)
    
    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        friends_list = get_friends_curr_user(current_user.token, current_user.user_id)
        return render_template('index.html', friends_list = friends_list)
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    user_id, token = oauth.callback()
    
    if user_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(user_id = user_id).first()
    
    if not user:
        username = get_concate_username(token, user_id)
        
        user = User(user_id = user_id, token = token, username = username)
        db.session.add(user)
        db.session.commit()
        
    login_user(user, True)
    return redirect(url_for('index'))

    
if __name__ == '__main__':
    db.create_all()
    app.run()
