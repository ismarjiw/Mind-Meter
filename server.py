from flask import (Flask, render_template, request, flash, session, redirect, jsonify, json)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import *
from passlib.hash import pbkdf2_sha256

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
    
    user = crud.check_hash_account(email, password)

    if user:
        flash("Welcome back! Happy meditating :)")
        session["email"] = email
        session["user_id"] = user.user_id
        return redirect("/profile")
    else:
        flash("Incorrect email or password. Please try to login again.")
        return redirect("/login")

@app.route("/logout")
def logout():
    """Logs out user"""

    session.pop('user_id', None)

    return redirect('/')

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
        user = crud.create_hash_account(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Happy meditating :)")
        session["email"] = email
        session["user_id"] = user.user_id

        return redirect("/profile")

@app.route("/profile")
def profile():
    """Renders profile page if a user logged in and displays if they've meditated the day before"""

    user = crud.get_user_by_id(session['user_id'])

    if 'user_id' not in session:
        return redirect("/login")

    show_streak = crud.on_streak(session['user_id'])

    if show_streak == True:
        streak = ["🔥 Great job, you're on a streak! Remember to meditate tomorrow 😌"]
    else:
        streak = ["It's okay to miss a day. Remember to meditate tomorrow 😌"]

    return render_template("profile.html", streak=streak, user=user)

@app.route("/profile/<user_id>", methods=('GET', 'POST'))
def profile_page(user_id):
    """View user profile journal page to add reflection to journal"""

    user = crud.get_user_by_id(user_id)
    users = crud.get_users()

    if 'meditation_id' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            tag = request.form['tag']
            tag = crud.create_tag(tag=tag)
            db.session.add(tag)
            db.session.commit()
            reflection = crud.create_reflection(meditation_id=session['meditation_id'],user_id=session['user_id'], title=title, content=content)
            reflection.tags.append(tag)
            db.session.add(reflection)
            db.session.commit()
            del session['meditation_id'] 
            return redirect ("/profile")
    else:
        flash('Please meditate again before trying to write a new reflection :)')
        return redirect ("/profile")

    return render_template('journal.html', user=user, users=users)

@app.route("/meditation", methods=['POST'])
def start_meditation():
    """Establishes meditation session and adds it to the database"""

    length = request.json.get('length')
    date = datetime.now()

    meditation = crud.create_meditation(session['user_id'], length=length, date=date)
    db.session.add(meditation)
    db.session.commit()
    session['meditation_id'] = meditation.meditation_id

    return {'meditation_id' : meditation.meditation_id}

    ##TODO: what is another way i can add meditation to session without printing meditation_id info to page?

@app.route("/journal")
def journal_entries():
    """Return all journal entries associated to specific user"""

    if 'user_id' in session:
        reflections = crud.get_reflections_by_id(user_id = session['user_id'])
    else:
        return redirect("/login")

    return render_template("all_reflections.html", reflections=reflections)

@app.route('/meditations_this_week.json')
def meditation_log():
    """Get meditation sessions date and length as JSON per user_id"""

    med_data = crud.get_time_length_meditation(session['user_id'])

    meditations_this_week = []
    for date, total in med_data.items():
        meditations_this_week.append({ 'date': date.isoformat(), 'length': total })

    return jsonify({'data':meditations_this_week})

@app.route('/delete-reflection/<meditation_id>')
def delete_reflection(meditation_id):
    """Delete reflection from journal"""

    if meditation_id != None:
        deleted_entry = crud.get_reflection_by_med_id(meditation_id)
        db.session.delete(deleted_entry)
        db.session.commit()
    else:
        flash("Unable to delete reflection.")
        
    return redirect("/journal")

@app.route('/delete-account/<user_id>')
def delete_account(user_id):
    """Delete account"""
    
    if user_id != None:
        account_to_delete = crud.get_user_by_id(session['user_id'])
        db.session.delete(account_to_delete)
        db.session.commit()
    else:
        flash('Unable to delete account.')

    return redirect ("/")

if __name__ == "__main__":
    connect_to_db(app, "meditations")
    app.run(host="0.0.0.0", debug=True)

