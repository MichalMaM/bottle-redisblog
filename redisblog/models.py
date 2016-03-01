import six

from .client import client
from .settings import URLS_MAPPING
from .utils import force_text

from .managers import Manager

# TODO: add to redis settings
PROJECT_PREFIX = 'redisblog'


class ModelBase(type):
    """
    Metaclass for all models.
    """
    def __new__(cls, name, bases, attrs):
        new_class = super(ModelBase, cls).__new__(cls, name, bases, attrs)

        manager = getattr(new_class, 'objects', Manager(new_class))
        new_class.objects = manager.__class__(new_class)

        parents = [b for b in bases if isinstance(b, ModelBase)]

        if not parents:
            return new_class

        fields = {}
        for parent in parents:
            if hasattr(parent, 'fields'):
                fields.update(parent.fields)
        fields.update(getattr(new_class, 'fields', {}))
        new_class.fields = fields

        return new_class


class Model(six.with_metaclass(ModelBase)):
    app_name = 'redisblog'
    model_name = None
    pk = None

    fields = {
        'pk': int,
    }

    @classmethod
    def key_prefix(cls):
        return '%s_%s' % (PROJECT_PREFIX, cls.content_type())

    @classmethod
    def content_type(cls):
        return '%s_%s' % (cls.app_name, cls.model_name)

    @classmethod
    def get_keys_with_id(cls, pk):
        return {
            'attrs': '%s:objs:%s' % (cls.key_prefix(), pk),
        }

    @classmethod
    def get_keys(cls):
        return {
            'ids': '%s:ids' % cls.key_prefix(),
            'order_listing': '%s:order' % cls.key_prefix(),
        }

    def __init__(self, **kwargs):
        for key, func in self.fields.items():
            if key in kwargs:
                setattr(self, key, func(kwargs[key]))

    def add_to_data_structures(self, keys=None, pipe=None):
        pipe = pipe or client.pipeline()
        keys = keys or self.get_keys()

        # print(list(self.fields.items()))
        # print(vars(self))
        mapping = {f: func(getattr(self, f)) for f, func in self.fields.items()}

        print(self.fields)
        print(mapping)
        keys_with_id = self.get_keys_with_id(self.pk)
        pipe.hmset(keys_with_id['attrs'], mapping)
        # TODO: add time instead self.pk as score
        pipe.zadd(keys['order_listing'], '%s_%s' % (self.content_type, self.pk), self.pk)

        return pipe

    def remove_from_data_structures(self, keys=None, pipe=None):
        pipe = pipe or client.pipeline()
        keys = keys or self.get_keys()

        keys_with_id = self.get_keys_with_id(self.pk)
        pipe.delete(keys_with_id['attrs'])
        # TODO: add time instead self.pk as score
        pipe.zrem(keys['order_listing'], '%s_%s' % (self.content_type, self.pk))

        return pipe

    def save(self, pipe=None, commit=True):
        pipe = pipe or client.pipeline()

        keys = self.get_keys()

        if not self.pk:
            pipe.incr(keys['ids'])
            self.pk = pipe.execute()[-1]

        pipe = self.add_to_data_structures(keys, pipe)

        if commit:
            pipe.execute()
        else:
            return pipe

    def delete(self, pipe=None, commit=True):
        pipe = pipe or client.pipeline()

        keys = self.get_keys()

        if not self.pk:
            return

        pipe = self.remove_from_data_structures(keys, pipe)

        if commit:
            pipe.execute()
        else:
            return pipe


class Article(Model):
    model_name = 'article'

    fields = {
        'title': force_text,
        'content': force_text,
    }

    def get_absolute_url(self):
        return URLS_MAPPING['article_detail'].replace('<pk:int>', str(self.pk))

    def get_delete_url(self):
        return URLS_MAPPING['article_delete'].replace('<pk:int>', str(self.pk))

    def get_edit_url(self):
        return URLS_MAPPING['article_edit'].replace('<pk:int>', str(self.pk))
