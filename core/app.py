from bottle import (
    request,
    redirect,
    abort,
    template
)

from redisblog.settings import FULL_URLS_MAPPING

from .decorators import get_context
from .forms import update_obj_from_form


TEMPLATE_PREFIX = 'redisblog/templates/'


def get_object_or_404(model, pk):
    obj = model.objects.get_obj(pk)
    if not obj:
        abort(404, "Object not found")
    return obj


def create_or_update_object_factory(model, form_class):
    def create_or_update_object(pk=None):
        if pk:
            article = get_object_or_404(model, pk)
        else:
            article = None

        if request.method == 'POST':
            form = form_class(request.forms.decode(), obj=article)
            if form.validate():
                if article:
                    update_obj_from_form(article, form)
                else:
                    article = model(**form.data)
                article.save()
                return redirect(FULL_URLS_MAPPING['article_add_success'])
        else:
            form = form_class(obj=article)

        context = get_context(data={'form': form})
        return template('%(tp)s/%(mn)ss/create_%(mn)s.html' % {'tp': TEMPLATE_PREFIX, 'mn': model.__name__.lower()}, **context)

    return create_or_update_object


def create_object_success_factory(model):
    def create_object_success():
        context = get_context()
        return template('%(tp)s/%(mn)ss/create_%(mn)s_success.html' % {'tp': TEMPLATE_PREFIX, 'mn': model.__name__.lower()}, **context)

    return create_object_success


def delete_object_factory(model, redir_url):
    def delete_object(pk):
        obj = get_object_or_404(model, pk)
        obj.delete()
        return redirect(FULL_URLS_MAPPING[redir_url])

    return delete_object


def delete_object_success_factory(model):
    def delete_object_success():
        context = get_context()
        return template('%(tp)s/%(mn)ss/delete_%(mn)s_success.html' % {'tp': TEMPLATE_PREFIX, 'mn': model.__name__.lower()}, **context)

    return delete_object_success


def object_detail_factory(model):
    def object_detail(pk):
        obj = get_object_or_404(model, pk)
        model_name = model.__name__.lower()
        context = get_context(data={model_name: obj})
        return template('%(tp)s/%(mn)ss/%(mn)s_detail.html' % {'tp': TEMPLATE_PREFIX, 'mn': model_name}, **context)

    return object_detail
