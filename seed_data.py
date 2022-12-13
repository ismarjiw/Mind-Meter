"Script to seed database."""

import os
from random import choice, randint
from datetime import datetime

import crud
from model import User, Meditation, Reflection, Tag, Sound, connect_to_db, db
import server

os.system("dropdb meditations")
os.system('createdb meditations')

connect_to_db(server.app, "meditations")
db.create_all()

sally = User (
                email = 'sally@gmail.com',
                password = 'taco'
                )

tim = User (
                email = 'tim@gmail.com',
                password = 'bell'
                )

med1 = Meditation (
                length = 5,
                date = datetime.now(),
                )

med2 = Meditation (
                length = 10,
                date = datetime.now(),
                )

ref1 = Reflection (
                title = 'Happy day',
                content = 'Today was a good day'
                )

ref1.meditation = med1

ref2 = Reflection (
                title = 'Good day',
                content = 'I won $100!'
                )

ref2.meditation = med2

tag1 = Tag (
            tag= 'happy'
            )

# tag1.reflection = ref1

tag2 = Tag (
            tag= 'sad'
            )

# tag2.reflection = ref2

sound1 = Sound (
            url= 'https://www.youtube.com/watch?v=42M3esYyHdw',
            name = 'rain'
            )

sound2 = Sound (
            url= 'https://www.youtube.com/watch?v=fBVJoIbNjdQ',
            name = 'ambient'
            )

db.session.add_all([sally, tim, med1, med2, ref1, ref2, tag1, tag2, sound1, sound2])
db.session.commit()