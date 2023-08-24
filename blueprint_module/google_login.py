from flask import render_template,session,redirect,url_for,request
from flask import Blueprint
from flask import current_app
from flask_oauthlib.client import OAuth
import os
google_login_bpr = Blueprint('b2', __name__)
app=current_app
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

@google_login_bpr.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('b2.authorized', _external=True))

@google_login_bpr.route('/login/google/authorize')
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
   
    return redirect(url_for('b4.index'))

@google.tokengetter
def get_google_oauth_token():
   return session.get('google_token')