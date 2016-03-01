from wtforms.form import Form
from wtforms.fields import StringField, TextAreaField
from wtforms import validators


def update_obj_from_form(obj, form):
    for f_name, f_val in form.data.items():
        if f_name in obj.fields:
            setattr(obj, f_name, f_val)


class ArticleForm(Form):

    title = StringField(u'Title', validators=[validators.input_required()])
    content = TextAreaField(u'Content', validators=[validators.input_required()])
