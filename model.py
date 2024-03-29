"""Models for meditation app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    """User class"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)

    google_id = db.Column(db.String, nullable=True)
    picture = db.Column(db.String, nullable=True)

    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    meditations = db.relationship("Meditation", back_populates="users")
    reflections = db.relationship("Reflection", back_populates="users")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} password={self.password}>'


class Meditation(db.Model):
    """A meditation session"""

    __tablename__ = "meditations"

    meditation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    length = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    users = db.relationship("User", back_populates="meditations")

    reflection = db.relationship("Reflection", uselist=False, back_populates='meditation')

    def __repr__(self):
        return f'<Meditation meditation_id={self.meditation_id} length={self.length} date={self.date}>'


class Reflection(db.Model):
    """A journal reflection"""

    __tablename__ = "reflections"

    meditation_id = db.Column(db.Integer, db.ForeignKey("meditations.meditation_id"), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    users = db.relationship("User", uselist=False,back_populates="reflections")

    meditation = db.relationship("Meditation", uselist=False, back_populates='reflection')
    tags = db.relationship("Tag", secondary='reflection_tags', back_populates="reflections")


    def __repr__(self):
        return f'<Reflection id={self.meditation_id} title={self.title}>'


class ReflectionTag(db.Model):
    """Tag of a specific reflection"""

    __tablename__ = 'reflection_tags'

    reflection_tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    reflection_id = db.Column(db.Integer, db.ForeignKey("reflections.meditation_id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"), nullable=False)
    
    def __repr__(self):
        return f"<ReflectionTag reflection_id = {self.reflection_id} tag_id = {self.tag_id}>"


class Tag(db.Model):
    """A journal tag"""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    
    tag = db.Column(db.String) 

    reflections = db.relationship("Reflection", secondary='reflection_tags', back_populates="tags")

    def __repr__(self):
        return f"{self.tag}"


def connect_to_db(app, db_name):
    """Connect to database"""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    
    connect_to_db(app, "meditations")