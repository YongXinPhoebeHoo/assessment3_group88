from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import Events, Comment, Booking
from .forms import EventsForm, CommentForm
import os
from .forms import CommentForm  
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from .events import generate_invoice
from . import db

main_bp = Blueprint('main', __name__)

# Index page with all events
@main_bp.route('/')
def index():
    events = Events.query.all()    
    return render_template('index.html', events=events)

# Get input from search bar to return relevant events
@main_bp.route('/search', methods=['GET'])
def search():
    input = request.args.get('name')  
    results = Events.query.filter(Events.event_name.ilike(f'%{input}%')).all()
    return render_template('search_result.html', results=results, input=input)

# Get input from drop down type and category to return relavent events
@main_bp.route('/searchothers', methods=['GET'])
def searchothers():
    type = request.args.get('type')
    category = request.args.get('category')
    results = Events.query.filter(Events.event_type.ilike(f'%{type}%'), Events.event_category.ilike(f'%{category}%')).all()
    return render_template('search_result.html', results=results)

# Ask for user to login
@main_bp.route('/event_create_update', methods=['GET', 'POST'])
@login_required
def event_create_update():
    form = EventsForm()
    if form.validate_on_submit():
        status = "Open"
        db_file_path = check_upload_file(form)
        event = Events(
            event_name=form.event_name.data,
            event_description=form.event_description.data,
            organiser_name=form.organiser_name.data,
            host_info=form.host_info.data,
            event_type=form.event_type.data,
            event_category=form.event_category.data,
            start_date=form.start_date.data,
            start_time=form.start_time.data,
            end_date=form.end_date.data,
            end_time=form.end_time.data,
            status=status,
            location=form.location.data,
            tickets=form.tickets.data,
            cost=form.cost.data,
            image=db_file_path,
            user_id=current_user.user_id
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('main.index'))    
    return render_template('event_create_update.html', form=form)

# Loads event details with event id
@main_bp.route('/event_details/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = Events.query.get_or_404(event_id)
    form = CommentForm()
    comments = Comment.query.filter_by(event_id=event_id).all()
    return render_template('event_details.html', event=event, form=form, comments=comments)

# Check if image file is uploaded 
def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename
  BASE_PATH = os.path.dirname(__file__)
  upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
  db_upload_path = '/static/img/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

# Upload comment in event detail
@main_bp.route('/event_details/<int:event_id>/comment', methods=['POST'])
@login_required
def post_comment(event_id):
    event = Events.query.get_or_404(event_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment=form.text.data,
            event_id=event.event_id,
            user_id=current_user.user_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
    return redirect(url_for('main.event_details', event_id=event_id))

# Ticket booking
@main_bp.route("/booking", methods=["GET", "POST"])
@login_required
def booking():
    event_id = request.form["event_id"]
    try:
        no_tickets = int(request.form["no_tickets"])
    except ValueError:
        return "Invalid input. Please provide a valid number."
    user_id = current_user.user_id
    bookings = Booking.query.filter_by(user_id=user_id).all()
    event = Events.query.get_or_404(event_id)
    purchase_date = datetime.now()
    prev_record = Booking.query.order_by(Booking.book_id.desc()).first()
    if prev_record and prev_record.invoice_no:
        current_numeric_part = int(prev_record.invoice_no[3:])
    else:
        current_numeric_part = 123
    invoice_no = generate_invoice(current_numeric_part)
    total_cost = (int(event.cost.replace("$", ""))) * no_tickets
    new_booking = Booking(
        user_id=user_id,
        event_id=event_id,
        event_name=event.event_name,
        no_tickets=no_tickets,
        purchase_date=purchase_date.replace(second=0, microsecond=0),
        invoice_no=invoice_no,
        invoice_date=(purchase_date + timedelta(days=1)).replace(
            second=0, microsecond=0
        ),
        total_cost=total_cost,
    )
    db.session.add(new_booking)
    if invoice_no and event:
        event.tickets = event.tickets - new_booking.no_tickets
    db.session.commit()
    print(event)
    return render_template(
        "booking.html",
        bookings=bookings,
        new_booking=new_booking,
        event=event,
        no_tickets=no_tickets,
    )

# Show all previous booking
@main_bp.route('/allbooking/<int:user_id>', methods=['GET'])
def allbooking(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return render_template("view_booking.html", bookings=bookings)

# Show events created by the user
@main_bp.route('/view_self_event')
@login_required
def view_self_event():
    events = Events.query.all()
    current_user_id = current_user.user_id
    events = Events.query.filter_by(user_id=current_user_id).all()
    return render_template('view_self_event.html', events=events)

# Update user's event
@main_bp.route('/event_update/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_update(event_id):
    event = Events.query.get_or_404(event_id)
    form = EventsForm(obj=event)
    if request.method == 'POST':
        print("MEOW Form is valid")
        event.event_name = form.event_name.data
        event.event_description = form.event_description.data
        event.organiser_name=form.organiser_name.data
        event.host_info=form.host_info.data
        event.event_type=form.event_type.data
        event.event_category=form.event_category.data
        event.start_date = form.start_date.data
        event.start_time = form.start_time.data
        event.end_date = form.end_date.data
        event.end_time = form.end_time.data
        event.location=form.location.data
        event.tickets=form.tickets.data
        event.cost=form.cost.data
        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('event_update.html', form=form, event=event)