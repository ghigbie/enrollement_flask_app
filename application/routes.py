from application import app, db
from flask import render_template, request, Response, json, flash, redirect, url_for
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
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password): #chekcs password agains password hash
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect(url_for("index"))
        else:
            flash("Sorry, something went wrong : (", "danger")
    return render_template("login.html", form=form, title="Login", login_nav=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Spring 2020"
    classes = Course.objects.order_by("+courseID")
    if len(classes) is 0:
        classes = course_data
    return render_template("courses.html", course_data=classes, courses=True, term=term)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form, title="Register", register=True)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('courseTitle')
    user_id = 1

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"You are already registered in this course, {courseTitle}.", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID)
            flash(f"You are successfully enrolled in {courseTitle}!", "sucess")
    classes = None
    
    term = request.form.get('term')

    return render_template("enrollment.html", enrollment=True, classes=classes)

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
