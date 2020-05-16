from application import app
from flask import render_template

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html", login=True)

@app.route("/login")
def index():
    return render_template("login.html")

@app.route("/courses")
def index():
    return render_template("courses.html")

@app.route("/register")
def index():
    return render_template("ergister.html")