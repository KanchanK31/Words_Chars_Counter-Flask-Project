from flask import session,redirect,url_for,request
from flask import Blueprint
from flask import current_app
from dotenv import load_dotenv
from flask_oauthlib.client import OAuth
import os
load_dotenv()

github_login_bpr = Blueprint('b3', __name__)
app=current_app
oauth = OAuth(app)
github = oauth.remote_app(
    'github',
    consumer_key=os.getenv('GITHUB_CONSUMER_KEY'),
    consumer_secret=os.getenv('GITHUB_CONSUMER_SECRET'),
    request_token_params={'scope': 'user:email'},  # You can modify scopes as needed
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

@github_login_bpr.route('/login/github')
def login_github():
    return github.authorize(callback=url_for('b3.authorized_git', _external=True))


@github_login_bpr.route('/login/github/authorize')
def authorized_git():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['github_token'] = response['access_token']
    print("******************")
    print(response.get('access_token'))
    print("******************")
    user_data = github.get('user').data
    # session['github_user'] = {
    #     'login': user_data.get('login'),
    #     'name': user_data.get('name'),
    #     'email': user_data.get('email')
    # }
    
    return redirect(url_for('b4.index'))

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')
