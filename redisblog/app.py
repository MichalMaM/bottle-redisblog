from bottle import (
    Bottle, request,
    redirect, view,
    static_file, abort,
    template
)

from .settings import URLS_MAPPING, STATIC_URL, STATIC_ROOT
from .decorators import add_base_context, get_context
from .models import Article
from .forms import ArticleForm, update_obj_from_form

app = Bottle()


def create_article(pk=None):
    if pk:
        article = Article.objects.get_obj(pk)
        if not article:
            abort(404, "Object not found")
    else:
        article = None

    if request.method == 'POST':
        print(article.pk)
        form = ArticleForm(request.forms.decode(), obj=article)
        if form.validate():
            if article:
                update_obj_from_form(article, form)
            else:
                article = Article(**form.data)
            article.save()
            return redirect(URLS_MAPPING['article_add_success'])
    else:
        form = ArticleForm(obj=article)

    context = get_context(data={'form': form})
    return template('redisblog/templates/create_article.html', **context)

create_article_get = app.get(URLS_MAPPING['article_add'])(create_article)
create_article_post = app.post(URLS_MAPPING['article_add'])(create_article)
edit_article_get = app.get(URLS_MAPPING['article_edit'])(create_article)
edit_article_post = app.post(URLS_MAPPING['article_edit'])(create_article)


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
