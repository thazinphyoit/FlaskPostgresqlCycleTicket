from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

# app 

app = Flask("__name__")

# secretkey 

app.secret_key = "hahaSK"

# database 

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:P@ssw0rd@localhost:5432/NewCycleTicket"
db = SQLAlchemy(app)

# table

class Users(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
db.create_all()

# routes 

@app.route("/")
def home () :
    validUser = None
    if "username" in session :
        validUser = session["username"]
    return render_template("home.html", username=validUser)

@app.route("/register", methods = ["GET", "POST"])
def register () :
    if request.method == "POST" :
        username  = request.form["username"]
        password = request.form["password"]
        newUser = Users(username=username, password=password)
        db.session.add(newUser)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login () :
    if request.method == "POST" :
        username = request.form["username"]
        password = request.form["password"]
        loginUser = Users.query.filter_by(username=username).first()
        print(loginUser)
        if loginUser :
            session["username"] = loginUser.username
            return redirect('/')
    return render_template("login.html")

@app.route("/logout")
def logout () :
    session.pop("username", None)
    return redirect("/")

# run 

if __name__ == "__main__" :
    app.run(debug=True)