from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import time 

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('index.html')


if __name__ == "__main__":
    connect_to_db(app, "meditations")
    app.run(host="0.0.0.0", debug=True)