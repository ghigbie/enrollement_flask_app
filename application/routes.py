from application import app, db
from flask import render_template, request, Response, json
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

course_data = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html", login=True, index=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form, title="Login", login_nav=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="2020"):
    return render_template("courses.html", course_data=course_data, courses=True, term=term)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form, title="Register", register=True)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('courseTitle')
    term = request.form.get('term')
    data = {
        "id": id,
        "title": title,
        "term": term
    }
    return render_template("enrollment.html", enrollment=True, data=data)

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = course_data
    else:
        jdata = course_data[int(idx)] #idx is coming back from url as a string, and it must be cast as an index
    
    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
   # User(user_id=3, first_name="Ben", last_name="Hur", email="benhur@gmail.com", password="abc1234").save()
   # User(user_id=4, first_name="Mary", last_name="Hur", email="maryhur@gmail.com", password="abc1234").save()
    users = User.objects.all()
    return render_template("user.html", users=users)
