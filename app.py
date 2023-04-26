from flask import Flask, render_template, redirect, url_for, request, session, flash
from repository import *
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = 'CareewiseProjectApplication'

db=CareerManagerDB()

@app.route('/')
def index():
    return "<h1>Hello World</h1>"

if __name__ == '__main__':
    app.run(debug = True)

