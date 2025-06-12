from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Project Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    demo_url = StringField('Demo URL', validators=[Optional(), URL()])
    tags = StringField('Tags (comma-separated)', validators=[Optional()])
    submit = SubmitField('Save Project')

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    is_published = BooleanField('Publish Post', default=True)
    submit = SubmitField('Save Post') 