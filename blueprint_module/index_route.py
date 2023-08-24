from flask import render_template,session,redirect,url_for
from flask import Blueprint
from flask import current_app

from functools import wraps
from datetime import date
from blueprint_module.github_login import github,get_github_oauth_token
from blueprint_module.google_login import google,get_google_oauth_token

index_bpr = Blueprint('b4', __name__)
app=current_app

datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


def login_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if 'github_token' not in session and 'google_token' not in session:
            return redirect(url_for('b1.public_index'))
        return view_func(*args, **kwargs)
    return decorated_view

@index_bpr.route('/',methods=['GET','POST'])
@login_required
def index():
    if 'google_token' in session:
        user_info = google.get('userinfo')
        # print(user_info.data.items())
        # print('\n\n\n\n')
        user_email= user_info.data['email']
        user_name=user_email.split('@')[0]

        # token=session['google_token']
        token=get_google_oauth_token()
        return render_template('index.html', user_name=user_name,datetoday2=datetoday2,token=token)
    if 'github_token' in session:
        user_info=github.get('user').data
        # print('\n\n\n\n')
        # print(user_info)
        # print('\n\n\n\n')
        user_name=user_info['login']
        token=get_github_oauth_token()
        return render_template('index.html', user_name=user_name,datetoday2=datetoday2,token=token)
