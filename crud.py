from model import db, User, Meditation, Reflection, Tag, Sound, SongPlay, connect_to_db
from flask import json
from datetime import datetime


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_users():
    """Return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Return user by id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def check_user_by_password(password, email):
    """Return a user by password."""
    
    user = User.query.filter(User.email == email).first()
    if user.password == password:
        return user 
    else:
        return False 


def create_meditation(user_id, length, date):
    """Create and return a new meditation session."""

    meditation = Meditation(user_id=user_id, length=length, date=date)

    return meditation

def get_meditation_by_id(meditation_id):
    """Return meditation by id"""

    return Meditation.query.get(meditation_id)

def all_meditation_dates(user_id):
    """Return all meditation dates by user_id"""

    all_dates = db.session.query(Meditation.date)
    user_dates = all_dates.filter(Meditation.user_id == user_id)

    return user_dates.all()

def all_meditation_lengths(user_id):
    """Return all meditation session lengths by user_id"""

    all_lengths = db.session.query(db.func.sum(Meditation.length), Meditation.date).group_by(Meditation.date)
    user_lengths = all_lengths.filter(Meditation.user_id == user_id)

    return user_lengths.all()

def create_reflection(meditation_id, user_id, title, content):
    """Create and return a new reflection"""

    reflection = Reflection(meditation_id=meditation_id, user_id=user_id, title=title, content=content)

    return reflection
    
def get_all_reflections():
    """Return all reflections"""

    return Reflection.query.all()

def get_reflections_by_id(user_id):
    """Return reflections by user id"""

    return Reflection.query.filter_by(user_id = user_id)

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

def create_sound(url, name):
    """Create and return a sound"""

    sound = Sound(url=url, name=name)

    return sound

### def for SongPlay if can connect to Spotify API


if __name__ == '__main__':
    from server import app
    connect_to_db(app)