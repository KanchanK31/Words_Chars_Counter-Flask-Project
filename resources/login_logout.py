from flask.views import MethodView
from flask import Flask, redirect, render_template,session,url_for
from flask_smorest import Blueprint
blp = Blueprint("login", __name__, description="Operations on login")

@blp.route("/login")
def public_index():
    return render_template('login.html')

@blp.route('/logout')
def logout():
    if 'google_token' in session:
        session.pop('google_token', None)
    if 'github_token' in session:
        session.pop('github_token', None)
    return redirect(url_for('public_index'))