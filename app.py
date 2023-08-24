import os
from dotenv import load_dotenv
import requests
from functools import wraps
from flask import Flask, redirect, render_template, session, url_for,request,jsonify
from resources.login_logout import blp
from resources.google_login import google_blp,google
from resources.github_login import github_blp,github
from flask_oauthlib.client import OAuth
from datetime import date

load_dotenv()

app = Flask(__name__)
app.register_blueprint(blp)
app.secret_key = os.urandom(24)  

datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

def replace_multiple_newlines(text):
    lines = text.split('\n')
    lines = [line for line in lines if line.strip()]
    return len(lines)

oauth = OAuth(app)
# google = oauth.remote_app(
#     'google',
#     consumer_key=os.getenv('GOOGLE_CONSUMER_KEY'),
#     consumer_secret=os.getenv('GOOGLE_CONSUMER_SECRET'),
#     request_token_params={
#         'scope': 'email',
#     },
#     base_url='https://www.googleapis.com/oauth2/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
    
# )

# github = oauth.remote_app(
#     'github',
#     consumer_key=os.getenv('GITHUB_CONSUMER_KEY'),
#     consumer_secret=os.getenv('GITHUB_CONSUMER_SECRET'),
#     request_token_params={'scope': 'user:email'},  # You can modify scopes as needed
#     base_url='https://api.github.com/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://github.com/login/oauth/access_token',
#     authorize_url='https://github.com/login/oauth/authorize',
# )

def login_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if 'github_token' not in session and 'google_token' not in session:
            return redirect(url_for('public_index'))
        return view_func(*args, **kwargs)
    return decorated_view

@app.route('/',methods=['GET','POST'])
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

def validate_token(token):
    google_introspection_url = "https://oauth2.googleapis.com/tokeninfo"
    google_params = {"access_token": token}


    github_introspection_url = "https://api.github.com/user"
    github_headers = {"Authorization": f"Bearer {token}"}

    
    # response = requests.get(introspection_url, params=params)
    google_response = requests.get(google_introspection_url, params=google_params)
    github_response = requests.get(github_introspection_url, headers=github_headers)

    if google_response.status_code == 200:
        token_info = google_response.json()
        if token_info.get("aud") == os.getenv('GOOGLE_CONSUMER_KEY'):
            # Replace 'YOUR_CLIENT_ID' with your actual Google OAuth client ID
            if not token_info.get("error"):
                # Check if the token is not expired
                if "expires_in" in token_info:
                    expires_in = int(token_info["expires_in"])
                    if expires_in > 0:
                        return True
    elif github_response.status_code == 200:
        github_info = github_response.json()
        if "login" in github_info:
            return True
    
    else:
        return False
    


def requires_valid_token(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        try:
            # Check if 'Authorization' header is present
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]  # Extract the token part

                # Validate the token
                if validate_token(token):
                    return view_func(*args, **kwargs)
                else:
                    return "Unauthorized", 401  # Unauthorized status code
            else:
                return "Unauthorized", 401  # Unauthorized status code

        except Exception as e:
            return "An error occurred: " + str(e), 500

    return decorated_function


# Here we'll ask google whether this given token is valid and is not expired and its client id is same as this App


@app.route('/count',methods=['POST'])
@requires_valid_token
def count():
    try:
        text = request.form['text']
        words = len(text.split())
        
        paras = replace_multiple_newlines(text)
        text = text.replace('\r', '')
        text = text.replace('\n', '')
        chars = len(text)
        
        # Assuming datetoday2 is defined somewhere in your code
        datetoday2 = ...  # Replace this with the actual value
        print("************")
        print(words)
        print(chars)
        print("***************")
        data={'words':words,'paras':paras,'chars':chars}
        # return render_template('index.html', data=data, datetoday2=datetoday2)
        return data
    
    except KeyError:
        error_message = "Text not found in the request form."
        return error_message

    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return error_message

# @app.route('/login')
# def public_index():
#     return render_template('login.html')


# @app.route('/login/google')
# def login_google():
#     return google.authorize(callback=url_for('authorized', _external=True))

# @app.route('/login/github')
# def login_github():
#     return github.authorize(callback=url_for('authorized_git', _external=True))

# Function to create GitHub OAuth session



# @app.route('/logout')
# def logout():
#     if 'google_token' in session:
#         session.pop('google_token', None)
#     if 'github_token' in session:
#         session.pop('github_token', None)
#     return redirect(url_for('public_index'))


# @app.route('/login/google/authorize')
# def authorized():
#     response = google.authorized_response()
#     if response is None or response.get('access_token') is None:
#         return 'Access denied: reason={} error={}'.format(
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     print("******************")
#     print(response.get('access_token'))
#     print("******************")
#     session['google_token'] = response['access_token']
   
#     return redirect(url_for('index'))

# @app.route('/login/github/authorize')
# def authorized_git():
#     response = github.authorized_response()
#     if response is None or response.get('access_token') is None:
#         return 'Access denied: reason={} error={}'.format(
#             request.args['error_reason'],
#             request.args['error_description']
#         )

#     session['github_token'] = response['access_token']
#     print("******************")
#     print(response.get('access_token'))
#     print("******************")
#     user_data = github.get('user').data
#     # session['github_user'] = {
#     #     'login': user_data.get('login'),
#     #     'name': user_data.get('name'),
#     #     'email': user_data.get('email')
#     # }
    
#     return redirect(url_for('index'))


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')



@google.tokengetter
def get_google_oauth_token():
   return session.get('google_token')

if __name__ == '__main__':
    app.run()
