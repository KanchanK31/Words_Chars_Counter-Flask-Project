from flask import request
from flask import Blueprint
from flask import current_app
from flask_oauthlib.client import OAuth
from functools import wraps
from dotenv import load_dotenv
import os
import requests
load_dotenv()
count_bpr = Blueprint('b5', __name__)
app=current_app
oauth = OAuth(app)

def replace_multiple_newlines(text):
    lines = text.split('\n')
    lines = [line for line in lines if line.strip()]
    return len(lines)

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


@count_bpr.route('/count',methods=['POST'])
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
