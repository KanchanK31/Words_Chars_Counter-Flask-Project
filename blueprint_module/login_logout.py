from flask import render_template,session,redirect,url_for
from flask import Blueprint

blueprint = Blueprint('b1', __name__)
@blueprint.route("/login", methods=['GET'])
def public_index():
    return render_template('login.html')

@blueprint.route('/logout')
def logout():
    if 'google_token' in session:
        session.pop('google_token', None)
    if 'github_token' in session:
        session.pop('github_token', None)
    return redirect(url_for('b1.public_index'))
