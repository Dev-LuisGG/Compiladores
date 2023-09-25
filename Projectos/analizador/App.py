from flask import Flask
app = Flask (__name__)

@app.route('/')

def index():
    return '<h1> hola mundo </h1>'

@app.route('/login')

def login():
    return 'login'
