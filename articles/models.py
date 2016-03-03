from core.utils import force_text
from core.models import Model, get_url


class Article(Model):
    model_name = 'article'

    fields = {
        'title': force_text,
        'content': force_text,
    }

    def get_absolute_url(self):
        return get_url('article_detail', self)

    def get_delete_url(self):
        return get_url('article_delete', self)

    def get_edit_url(self):
        return get_url('article_edit', self)
