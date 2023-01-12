from model import db, User, Meditation, Reflection, Tag, connect_to_db
from flask import json
from datetime import *
from sqlalchemy import desc
from passlib.hash import pbkdf2_sha256


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_google_user(google_id, email, picture):

    google_user = User(google_id=google_id, email=email, picture=picture)

    return google_user 

def check_google_user(email):

    google_user = User.query.filter(User.email == email).first()

    if google_user:
        return google_user
    else:
        return False

def get_users():
    """Return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Return user by id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_hash_account(email, password):
    """Hashes password"""

    hashed_password = pbkdf2_sha256.hash(password)

    user = User(email=email, password=hashed_password)

    return user

def check_hash_account(email, password):
    """Check if hashed pw in db matches entered password"""

    user = User.query.filter(User.email == email).first()

    if pbkdf2_sha256.verify(password, user.password):
        return user
    else:
        return False

def check_user_by_password(password, email):
    """Return a user by password."""
    
    user = User.query.filter(User.email == email).first()

    if user.password == password:
        return user 
    elif user.password != password:
        return False 

def create_meditation(user_id, length, date):
    """Create and return a new meditation session."""

    meditation = Meditation(user_id=user_id, length=length, date=date)

    return meditation

def get_meditation_by_id(meditation_id):
    """Return meditation by id"""

    return Meditation.query.get(meditation_id)

def get_time_length_meditation(user_id):
    """Returns date and total length of meditation sessions per day"""

    user = User.query.get(user_id)
    
    when_time_meditated = {}

    for meditation in user.meditations:
        if meditation.date.date() == meditation.date.date():
            if meditation.date.date() in when_time_meditated:
                when_time_meditated[meditation.date.date()] += meditation.length
            else:
                when_time_meditated[meditation.date.date()] = meditation.length

    return when_time_meditated

def on_streak(user_id):
    """Display 'on streak' if user logged meditation session today and yesterday"""

    user = User.query.get(user_id)
    streak = False 
    today = date.today()
    yesterday = date.today() - timedelta(days = 1)
    meditation_dates = []

    for meditation in user.meditations:
        meditation_dates.append(meditation.date.date())
    if today and yesterday in meditation_dates:
        streak = True

    return streak

def create_reflection(meditation_id, user_id, title, content):
    """Create and return a new reflection"""

    reflection = Reflection(meditation_id=meditation_id, user_id=user_id, title=title, content=content)

    return reflection
    
def get_all_reflections():
    """Return all reflections"""

    return Reflection.query.all()

def get_reflections_by_id(user_id):
    """Return reflections by user id"""

    return Reflection.query.filter_by(user_id = user_id).order_by(Reflection.meditation_id.desc())

def get_reflection_by_med_id(meditation_id):
    """Return reflection by meditation id"""

    return Reflection.query.filter_by(meditation_id = meditation_id).first()

def create_tag(tag):
    """Create and return a new tag"""

    tag = Tag(tag=tag)

    return tag

def get_tags():
    """Return all tags"""

    return Tag.query.all()

def get_tag_by_id(meditation_id):
    """Return tags by meditation id"""

    return Tag.query.filter_by(meditation_id=meditation_id).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)