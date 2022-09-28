
from flask import Flask, session
from flask_debugtoolbar import DebugToolbarExtension

from forms import (
    UserAddForm, UserEditForm, LoginForm, MessageForm,
)

from warbler.root import CSRFProtection, LoginForm

from models import (
    db, connect_db, User, Message, DEFAULT_IMAGE_URL, DEFAULT_HEADER_IMAGE_URL)

from warbler.messages.views import messages
from warbler.users.views import users
import os

from dotenv import load_dotenv




app = Flask(__name__)
app.register_blueprint(messages, url_prefix="/messages" )
app.register_blueprint(users, url_prefix="/users")

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it."""

    g.csrf_form = CSRFProtection()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

