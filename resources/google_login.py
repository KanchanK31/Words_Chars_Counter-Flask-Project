import os
from flask import redirect,session,url_for,request
from flask_smorest import Blueprint
from flask_oauthlib.client import OAuth

from __main__ import app
google_blp = Blueprint("google", __name__, description="Operations related to google login")

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv('GOOGLE_CONSUMER_KEY'),
    consumer_secret=os.getenv('GOOGLE_CONSUMER_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    
)

@google_blp.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('authorized', _external=True))


@google_blp.route('/login/google/authorize')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    print("******************")
    print(response.get('access_token'))
    print("******************")
    session['google_token'] = response['access_token']
   
    return redirect(url_for('index'))


