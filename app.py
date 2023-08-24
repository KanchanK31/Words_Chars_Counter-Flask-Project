import os
from dotenv import load_dotenv
from flask import Flask


from blueprint_module.login_logout import blueprint
from blueprint_module.google_login import google_login_bpr
from blueprint_module.github_login import github_login_bpr
from blueprint_module.index_route import index_bpr
from blueprint_module.count import count_bpr

load_dotenv()

app = Flask(__name__)
app.register_blueprint(blueprint)
app.register_blueprint(google_login_bpr)
app.register_blueprint(github_login_bpr)
app.register_blueprint(index_bpr)
app.register_blueprint(count_bpr)

app.secret_key = os.urandom(24)  



if __name__ == '__main__':
    app.run()
