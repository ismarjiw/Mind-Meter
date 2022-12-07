from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import time 

app = Flask(__name__)

app.secret_key = "hackbright"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('index.html')

@app.route("/login")
def login_page():
    """Login page"""

    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def user_login_page():
    """Logs in the user"""

    password = request.form.get("password")
    email = request.form.get("email")
    user_password = crud.check_user_by_password(password, email)

    ## how to get to specific user profile page after logging in ##

    if user_password:
        flash("Welcome back! Happy meditating :)")
        session["email"] = email
        return render_template("profile.html")
    else:
        flash("Incorrect email or password. Please try to login again.")
        return redirect("/login")
        

@app.route("/register", methods=["POST"])
def register_user():
    """Registers new user"""
    
    password = request.form.get("password")
    email = request.form.get("email")
    user = crud.get_user_by_email(email)

    if user:
        flash("Account already created. Please login.")
        return redirect("/login")
    elif user == None:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Happy meditating :)")
        session["email"] = email
        return render_template("profile.html")

@app.route("/profile/<user_id>")
def profile_page(user_id):
    """View user profile page after login"""

    user = crud.get_user_by_id(user_id)

    return render_template('profile.html', user=user)

if __name__ == "__main__":
    connect_to_db(app, "meditations")
    app.run(host="0.0.0.0", debug=True)