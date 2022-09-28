from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from users import User

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "/static/images/default-pic.png"
DEFAULT_HEADER_IMAGE_URL = "/static/images/warbler-hero.jpg"

def __repr__(self):
    return f"<User #{self.id}: {self.username}, {self.email}>"


@classmethod
def signup(cls, username, email, password, image_url=DEFAULT_IMAGE_URL):
    """Sign up user.

    Hashes password and adds user to system.
    """

    hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    user = User(
        username=username,
        email=email,
        password=hashed_pwd,
        image_url=image_url,
    )

    db.session.add(user)
    return user


@classmethod
def authenticate(cls, username, password):
    """Find user with `username` and `password`.

    This is a class method (call it on the class, not an individual user.)
    It searches for a user whose password hash matches this password
    and, if it finds such a user, returns that user object.

    If this can't find matching user (or if password is wrong), returns
    False.
    """

    user = cls.query.filter_by(username=username).first()

    if user:
        is_auth = bcrypt.check_password_hash(user.password, password)
        if is_auth:
            return user

    return False
