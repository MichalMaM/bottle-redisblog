from wtforms.form import Form
from wtforms.fields import StringField, TextAreaField
from wtforms import validators


class ArticleForm(Form):

    title = StringField(u'Title', validators=[validators.input_required()])
    content = TextAreaField(u'Content', validators=[validators.input_required()])
