from flask import Flask
from new_demo.app.config import Config
app = Flask(__name__)
app.config.from_object(Config)
# print("SECRET KEY IS: ", app.config["SECRET_KEY"])

@app.route('/')
@app.route('/home')
def hello():
    return f'<h1>{app.config["GREETING"]}</h1>'

@app.route('/about')
def about():
    return '<h1>About</h1>'

@app.route('/item/<id>')
def item(id):
    return f'<h1>Item {id}</h1>'

@app.before_request
def before_request_function():
    print("before_request is running")

@app.after_request
def after_request_function(response):
    print("after_request is running")
    return response

@app.before_first_request
def before_first_function():
    print("before_first_request happens once")