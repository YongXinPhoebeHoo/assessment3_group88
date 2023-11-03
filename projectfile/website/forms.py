from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, RadioField, PasswordField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Event creation and update form
class EventsForm(FlaskForm):
    event_name = StringField('Event Name', validators=[InputRequired()], render_kw={"placeholder": "Be clear and descriptive"})
    event_description = StringField('Event Description', validators=[InputRequired()], render_kw={"placeholder":"Add details about your event (e.g. schedule)"})
    organiser_name = StringField('Organizer Name', validators=[InputRequired()], render_kw={"placeholder": "Tell attendees who is organising this event"})
    host_info = StringField('Host Information', validators=[InputRequired()], render_kw={"class": "form-control big_input", "placeholder": "Enter host information"})
    
    event_type = SelectField('Event Type', validators=[InputRequired()], choices=[
        ('','Type'),
        ('celebration', 'Celebration'),
        ('festival', 'Festival'),
        ('party', 'Party'),
        ('social_gather', 'Social Gathering')
    ])
  
    event_category = SelectField('Category Type', validators=[InputRequired()], choices=[
        ('', 'Category'),
        ('culture', 'Culture'),
        ('sport', 'Sport'),
        ('food_drink', 'Food & drink'),
        ('religion_spirituality', 'Religion & spirituality')
    ])

    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[InputRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[InputRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[InputRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[InputRequired()])

    location = StringField('Location', validators=[InputRequired()], render_kw={"placeholder": "Be clear and descriptive"})

    tickets = StringField('Available Tickets', validators=[InputRequired()], render_kw={"placeholder": "Enter number of available tickets"})
    cost = StringField('Cost', validators=[InputRequired()], render_kw={"placeholder": "Price ($)"})
    image = FileField('Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])

    submit = SubmitField("Create")

# Login form
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# Registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# Comment box/input
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create') 