from bottle import (
    Bottle,
    request,
    redirect,
    abort,
    template
)

from redisblog.settings import URLS_MAPPING, FULL_URLS_MAPPING

from core.decorators import get_context
from core.forms import update_obj_from_form

from .models import Article
from .forms import ArticleForm

TEMPLATE_PREFIX = 'redisblog/templates/articles'

app = Bottle()


def create_article(pk=None):
    if pk:
        article = Article.objects.get_obj(pk)
        if not article:
            abort(404, "Object not found")
    else:
        article = None

    if request.method == 'POST':
        form = ArticleForm(request.forms.decode(), obj=article)
        if form.validate():
            if article:
                update_obj_from_form(article, form)
            else:
                article = Article(**form.data)
            article.save()
            return redirect(FULL_URLS_MAPPING['article_add_success'])
    else:
        form = ArticleForm(obj=article)

    context = get_context(data={'form': form})
    return template('%s/create_article.html' % TEMPLATE_PREFIX, **context)

create_article_get = app.get(URLS_MAPPING['article_add'])(create_article)
create_article_post = app.post(URLS_MAPPING['article_add'])(create_article)
edit_article_get = app.get(URLS_MAPPING['article_edit'])(create_article)
edit_article_post = app.post(URLS_MAPPING['article_edit'])(create_article)


@app.route(URLS_MAPPING['article_add_success'])
def create_article_success():
    context = get_context()
    return template('%s/create_article_success.html' % TEMPLATE_PREFIX, **context)


@app.route(URLS_MAPPING['article_delete'])
def delete_article(pk):
    article = Article.objects.get_obj(pk)
    if not article:
        abort(404, "Object not found")
    article.delete()
    return redirect(FULL_URLS_MAPPING['article_delete_success'])


@app.route(URLS_MAPPING['article_delete_success'])
def delete_article_success():
    context = get_context()
    return template('%s/delete_article_success.html' % TEMPLATE_PREFIX, **context)


@app.route(URLS_MAPPING['article_detail'])
def article_detail(pk):
    article = Article.objects.get_obj(pk)
    if not article:
        abort(404, "Object not found")

    context = get_context(data={'article': Article.objects.get_obj(pk)})
    return template('%s/article_detail.html' % TEMPLATE_PREFIX, **context)
