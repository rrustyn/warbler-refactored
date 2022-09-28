from database import db

class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

def is_followed_by(self, other_user):
    """Is this user followed by `other_user`?"""

    found_user_list = [
        user for user in self.followers if user == other_user]
    return len(found_user_list) == 1

def is_following(self, other_user):
    """Is this user following `other_use`?"""

    found_user_list = [
        user for user in self.following if user == other_user]
    return len(found_user_list) == 1

