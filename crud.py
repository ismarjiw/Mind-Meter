from model import db, User, Meditation, Reflection, Tag, Sound, SongPlay, connect_to_db
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
    
    if User.query.filter(User.password == password).first() and User.query.filter(User.email == email).first():
        return True
    else:
        return False

def create_meditation(length, date):
    """Create and return a new meditation session."""

    meditation = Meditation(length=length, date=date)

    return meditation

def create_reflection(title, content):
    """Create and return a new reflection"""

    reflection = Reflection(title=title, content=content)

    return reflection

def create_tag(tag):
    """Create and return a new tag"""

    tag = Tag(tag=tag)

    return tag

def create_sound(url, name):
    """Create and return a sound"""

    sound = Sound(url=url, name=name)

    return sound

### def for SongPlay if can connect to Spotify API


if __name__ == '__main__':
    from server import app
    connect_to_db(app)