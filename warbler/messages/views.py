from models import Message
from forms import MessageForm
from database import db
from flask import Blueprint, flash, render_template, redirect

messages = Blueprint('messages', __name__,
                      template_folder="templates")
                      
##############################################################################
# Messages routes:

@messages.route('/messages/new', methods=["GET", "POST"])
def add_message():
    """Add a message:

    Show form if GET. If valid, update message and redirect to user page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(text=form.text.data)
        g.user.messages.append(msg)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('messages/create.html', form=form)


@messages.get('/messages/<int:message_id>')
def show_message(message_id):
    """Show a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    msg = Message.query.get_or_404(message_id)
    return render_template('messages/show.html', message=msg)


@messages.post('/messages/<int:message_id>/delete')
def delete_message(message_id):
    """Delete a message.

    Check that this message was written by the current user.
    Redirect to user page on success.
    """

    form = g.csrf_form

    if not form.validate_on_submit() or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    msg = Message.query.get_or_404(message_id)
    if msg.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(msg)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")
