from bottle import (
    Bottle, request,
    redirect, view,
    static_file, abort,
)

from .settings import URLS_MAPPING, STATIC_URL, STATIC_ROOT
from .decorators import add_base_context
from .models import Article

app = Bottle()


@app.get(URLS_MAPPING['article_add'])
@view('redisblog/templates/create_article.html')
@add_base_context()
def create_article():
    return {}


@app.post(URLS_MAPPING['article_add'])
def create_article_post():
    forms = request.forms.decode()
    title = forms.get('title')
    content = forms.get('content')
    # create article
    Article(title=title, content=content).save()
    return redirect(URLS_MAPPING['article_add_success'])


@app.route(URLS_MAPPING['article_add_success'])
@view('redisblog/templates/create_article_success.html')
@add_base_context()
def create_article_success():
    return {}


@app.route(URLS_MAPPING['article_delete'])
def delete_article(pk):
    article = Article.objects.get_obj(pk)
    if not article:
        abort(404, "Object not found")
    article.delete()
    return redirect(URLS_MAPPING['article_delete_success'])


@app.route(URLS_MAPPING['article_delete_success'])
@view('redisblog/templates/delete_article_success.html')
@add_base_context()
def delete_article_success():
    return {}


@app.route(URLS_MAPPING['article_detail'])
@view('redisblog/templates/article_detail.html')
@add_base_context()
def article_detail(pk):
    article = Article.objects.get_obj(pk)
    if not article:
        abort(404, "Object not found")
    return {
        'article': Article.objects.get_obj(pk),
    }


@app.route(URLS_MAPPING['hp'])
@view('redisblog/templates/hp.html')
@add_base_context()
def hp():
    return {
        'articles': Article.objects.get_last_objects()
    }


@app.error(404)
@view('redisblog/templates/404.html')
@add_base_context()
def error404(err):
    return {}


@app.route('%s<filepath:path>' % STATIC_URL)
def server_static(filepath):
    return static_file(filepath, root=STATIC_ROOT)
