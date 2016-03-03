from bottle import (
    Bottle,
)

from redisblog.settings import URLS_MAPPING

from core.app import (
    create_or_update_object_factory,
    create_object_success_factory,
    delete_object_factory,
    delete_object_success_factory,
    object_detail_factory,
)

from .models import Article
from .forms import ArticleForm

app = Bottle()


create_or_update_article = create_or_update_object_factory(Article, ArticleForm)

create_article_get = app.get(URLS_MAPPING['article_add'])(create_or_update_article)
create_article_post = app.post(URLS_MAPPING['article_add'])(create_or_update_article)
edit_article_get = app.get(URLS_MAPPING['article_edit'])(create_or_update_article)
edit_article_post = app.post(URLS_MAPPING['article_edit'])(create_or_update_article)

create_article_success = app.route(URLS_MAPPING['article_add_success'])(create_object_success_factory(Article))
delete_article = app.route(URLS_MAPPING['article_delete'])(delete_object_factory(Article, 'article_delete_success'))
delete_article_success = app.route(URLS_MAPPING['article_delete_success'])(delete_object_success_factory(Article))
article_detail = app.route(URLS_MAPPING['article_detail'])(object_detail_factory(Article))
