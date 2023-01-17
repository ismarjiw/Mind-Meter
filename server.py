import os 
import pathlib 
import urllib

from flask import (Flask, render_template, request, flash, abort, session, redirect, Response, jsonify, json)
from flask_session import Session
import requests 
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import *
from passlib.hash import pbkdf2_sha256
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
from random import choice
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)
TOKEN_INFO = 'token_info'

FORTUNES = [
    "Start where you are. Use what you have. Do what you can.",
    "Putting yourself fully into what you do is a form of love.",
    "Do what you love. The rest will fall into place.",
    "Speak good things about yourself into existence.",
    "Let the difference between where you are and where you want to be inspire you.",
]

OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file = client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri = "http://127.0.0.1:5000/callback",
)

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
        flash("Welcome back! Happy meditating 🧘")
        session["email"] = email
        session["user_id"] = user.user_id
        return redirect("/profile")
    else:
        flash("Incorrect email or password. Please try again.")
        return redirect("/login")

@app.route('/google_login')
def google_login():
    """Initiates Google Oauth2 flow and returns auth url"""

    authorization_url, state = flow.authorization_url(
        access_type = 'offline', 
        include_granted_scopes = 'true',
        )

    return redirect(authorization_url)

@app.route("/callback")
def callback():
    """Returns auth response and logs in new or current Google user"""
    
    flow.fetch_token(authorization_response = request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token = credentials._id_token,
        request = token_request,
        audience = GOOGLE_CLIENT_ID
    )

    google_id = id_info.get("sub")
    email = id_info.get("email")
    picture = id_info.get("picture")

    user = crud.check_google_user(email)

    if user:
        flash("Welcome back! Happy meditating 🧘")
        session["email"] = email
        session["picture"] = picture
        session["user_id"] = user.user_id
        return redirect("/profile")
    else:
        user = crud.create_google_user(google_id, email, picture)
        db.session.add(user)
        db.session.commit()
        session["email"] = email
        session["picture"] = picture
        session["user_id"] = user.user_id
        flash('Account created! Happy meditating 🧘')
        return redirect("/profile")
        
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
        flash("Account created! Happy meditating 🧘")
        session["email"] = email
        session["user_id"] = user.user_id

        return redirect("/profile")

@app.route("/profile")
def profile():
    """Renders profile page if a user is logged in"""

    if 'user_id' not in session:
        return redirect("/login")

    user = crud.get_user_by_id(session["user_id"])
    
    if user == None:
        return render_template('404.html'), 404
    if user.picture:
        profile_picture = user.picture
    else:
        profile_picture = "../static/src/Photos/profile.png"

    show_streak = crud.on_streak(session['user_id'])

    fortune = random.choice(FORTUNES)

    if show_streak == True:
        streak = "🔥 Great job, you're on a streak! Remember to meditate tomorrow 😌"
    else:
        streak = "It's okay to miss a day. Remember to meditate tomorrow 😌"

    return render_template("profile.html", user=user, streak=streak, fortune=fortune, profile_picture=profile_picture)

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

@app.route("/reflection", methods=['POST'])
def submit_reflection():
    """Route for adding journal entry with React"""

    title = request.json.get("title")
    content = request.json.get("content")
    tag = request.json.get("tag")

    if 'meditation_id' in session:
        tag = crud.create_tag(tag=tag)
        db.session.add(tag)
        db.session.commit()
        reflection = crud.create_reflection(meditation_id=session['meditation_id'],user_id=session['user_id'], title=title, content=content)
        reflection.tags.append(tag)
        db.session.add(reflection)
        db.session.commit()
        del session['meditation_id']
        return {"status": 'Your reflection is saved 😌'}
    else:
        return {"status": 'Meditate again first'}

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

@app.route("/journal")
def journal_entries():
    """Return all journal entries associated to specific user"""

    if 'user_id' in session:
        reflections = crud.get_reflections_by_id(user_id = session['user_id'])
    else:
        return redirect("/login")

    page = request.args.get('page', 1, type=int)
    pagination = reflections.paginate(
        page, per_page=4)

    return render_template("all_reflections.html", pagination=pagination)

@app.route('/meditations_this_week.json')
def meditation_log():
    """Get meditation sessions date and length as JSON per user_id"""

    med_data = crud.get_time_length_meditation(session['user_id'])

    meditations_this_week = []
    for date, total in med_data.items():
        meditations_this_week.append({ 'date': date.isoformat(), 'length': total })

    return jsonify({'data': meditations_this_week})

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

@app.route('/weather', methods=['GET'])
def get_weather():
    """API call to OpenWeather that tells user temp/weather for given zipcode"""

    zipcode = request.args.get('zip')

    if not zipcode:
        abort(400, 'Missing argument zipcode')

    data = {}
    data['zip'] = request.args.get('zip')
    data['appid'] = OPEN_WEATHER_API_KEY
    data['units'] = 'imperial'

    url_values = urllib.parse.urlencode(data)
    url = 'http://api.openweathermap.org/data/2.5/weather'
    full_url = url + '?' + url_values
    data = urllib.request.urlopen(full_url)

    resp = Response(data)
    resp.status_code = 200

    return render_template('weather.html', title='Weather Info', data = json.loads(data.read().decode('utf8')))

# //////////////////////////////////////////////////////////////////////////

@app.route('/sign_in')
def index():
    """Initiates sign in to Spotify app"""

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-modify-playback-state', cache_handler=cache_handler, show_dialog=True)

    # Step 1. Display sign in link when no token
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render_template('spotify_sign_in.html', auth_url=auth_url)

    # Step 3. Signed in with token => display data
    if auth_manager.validate_token(cache_handler.get_cached_token()):
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        return render_template('spotify_signed_in.html', spotify=spotify)

# Step 2. Being redirected from Spotify auth page
@app.route('/redirect')
def redirectPage():
    """Handles redirect for Spotify API request"""

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-modify-playback-state', cache_handler=cache_handler, show_dialog=True)
    # session.clear()
    code = request.args.get('code')
    token_info = auth_manager.get_access_token(code)

    if token_info:
        session[TOKEN_INFO] = token_info
    else:
        token_info = auth_manager.refresh_access_token(code) 
        session[TOKEN_INFO] = token_info 

    return redirect("/profile")
    
@app.route('/sign_out')
def sign_out():
    """Signs user out of Spotify session"""

    session.pop("token_info", None)

    return redirect('/profile')

if __name__ == "__main__":
    connect_to_db(app, "meditations")
    app.run(host="0.0.0.0", debug=True, threaded=True)

