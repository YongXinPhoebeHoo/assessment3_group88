from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Events, Comment
from .forms import EventsForm, CommentForm
from . import db
import os, string, random
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

# Show all relevant information in event information
eventbp = Blueprint('events', __name__, url_prefix='/events')
@eventbp.route('/<id>')
def show(id):
    events = db.session.scalar(db.select(Events).where(Events.id==id))
    form = CommentForm()
    comments = events.comments.order_by(Comment.created_at.desc()).all()
    return render_template('events/show.html', events=events, form=form, comments=comments)

# User adds comments to an event
@eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()
    #get the destination object associated to the page and the comment
    events = db.session.scalar(db.select(Events).where(Events.id==id))
    if form.validate_on_submit():  
      comment = Comment.query.filter_by(event_id=id).all()
      db.session.add(comment) 
      db.session.commit() 
      flash('Your comment has been added', 'success')  
    return redirect(url_for('events.show', id=id, comment=comment))

# Show order details for booking 
def generate_invoice(number):
    letters = string.ascii_uppercase
    random_string = ''.join(random.choice(letters) for _ in range(3))
    new_number = number + 1
    invoice_no = f"{random_string}{new_number}"
    return invoice_no