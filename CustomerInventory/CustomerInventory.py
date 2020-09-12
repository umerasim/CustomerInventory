# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
from flask import Flask, render_template  # From module flask import class Flask
from flask.globals import request
app = Flask(__name__)    # Construct an instance of Flask class for our webapp

@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
#     return 'Hello, world!'
#     return render_template('j2_query.html')
    return render_template('j2_derived.html')


@app.route('/hello')
def hello():
    return 'Hello, world!'

@app.route('/hello/<username>')  # URL with a variable
def hello_username(username):    # The function shall take the URL variable as parameter
    return 'Hello, {}'.format(username)

@app.route('/hello/<int:userid>')  # Variable with type filter. Accept only int
def hello_userid(userid):          # The function shall take the URL variable as parameter
    return 'Hello, your ID is: {:d}'.format(userid)


@app.route('/process', methods=['POST'])
def process():
    # Retrieve the HTTP POST request parameter value from 'request.form' dictionary
    _username = request.form.get('username')  # get(attr) returns None if attr is not present
 
    # Validate and send response
    if _username:
        return render_template('j2_response.html', username=_username)
    else:
        return 'Please go back and enter your name...', 400  # 400 Bad Request



if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True)  # Launch built-in web server and run this Flask webapp