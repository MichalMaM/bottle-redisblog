from bottle import (
    Bottle,
    static_file,
    template
)


from core.decorators import get_context
from articles.models import Article
from articles.app import app as articles_app

from .settings import URLS_MAPPING, STATIC_URL, STATIC_ROOT, URL_PREFIXES

app = Bottle()
app.mount(URL_PREFIXES['article'], articles_app)


@app.route(URLS_MAPPING['hp'])
def hp():
    context = get_context(data={'articles': Article.objects.get_last_objects()})
    return template('redisblog/templates/hp.html', **context)


@app.error(404)
def error404(err):
    context = get_context()
    return template('redisblog/templates/404.html', **context)


@app.route('%s<filepath:path>' % STATIC_URL)
def server_static(filepath):
    return static_file(filepath, root=STATIC_ROOT)
