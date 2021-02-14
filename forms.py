from flask_wtf import FlaskForm, RecaptchaField
from wtforms import widgets, SelectMultipleField, StringField, PasswordField, TextAreaField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    """Form for adding users."""
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    image_url = StringField('Image URL')
    ##submit = SubmitButton('Sign Up')
    ##recaptcha = RecaptchaField()
    
class UserEditForm(FlaskForm):
    """Form for editing users."""
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    country = StringField('(Optional) Country')
    address = StringField('(Optional) address')
    city = StringField('(Optional) city')
    state = StringField('(Optional) state')
    province = StringField('(Optional) Province')
    gender = SelectField('(Optional) Gender', choices=[('male', 'male'),('female','female'),('other','other')])
    details = TextAreaField('(Optional) details')
    password = PasswordField('Password', validators=[Length(min=6)])
    ##submit = SubmitButton('Save Changes')
    
class LoginForm(FlaskForm):
    """Login form."""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    ##submit = SubmitButton('Login')
    
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class GenresLikedEditForm(FlaskForm):
    """Form for storing liked genres in order to pull recommendations"""
    
    genres = MultiCheckboxField('Genres', choices=[('Action','Action'), 
            ('Comedy','Comedy'), ('Drama','Drama'),('Fantasy','Fantasy'),
            ('Horror','Horror'),('Mystery','Mystery'),('Romance','Romance'), 
            ('Thriller','Thriller')])
    
    video_type = SelectField('Type', choices=[('TV Shows','TV Shows'), ('Movies','Movies')])
    
