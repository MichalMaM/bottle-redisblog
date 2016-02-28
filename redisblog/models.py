from .client import client
from .settings import URLS_MAPPING
from .utils import force_text

# TODO: add to redis settings
PROJECT_PREFIX = 'redisblog'


class BaseManagerMixin(object):

    @classmethod
    def get_last_objects(cls, offset=0, count=10, keys=None, pipe=None):
        pipe = pipe or client.pipeline()
        keys = keys or cls.get_keys()
        pipe.zrevrange(
            keys['order_listing'],
            start=offset,
            end=offset + count - 1,
            withscores=True
        )
        results = pipe.execute()

        for value, score in results[-1]:
            pk = int(force_text(value).rsplit('_',)[-1])
            obj = cls.get_obj(pk, pipe)
            if not obj:
                # TODO: add log
                continue
            yield obj

    @classmethod
    def get_obj(cls, pk, keys_with_id=None, pipe=None):
        # TODO: check if id exists
        pipe = pipe or client.pipeline()
        keys_with_id = keys_with_id or cls.get_keys_with_id(pk)
        pipe.hgetall(keys_with_id['attrs'])
        attrs_dict = {force_text(k): v for k, v in pipe.execute()[-1].items()}
        if not attrs_dict:
            return None
        return cls(**attrs_dict)


class BaseModel(BaseManagerMixin):
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


class Article(BaseModel):
    model_name = 'article'

    fields = {
        'pk': int,
        'title': force_text,
        'content': force_text,
    }

    def get_absolute_url(self):
        return URLS_MAPPING['article_detail'].replace('<pk:int>', str(self.pk))

    def get_delete_url(self):
        return URLS_MAPPING['article_delete'].replace('<pk:int>', str(self.pk))
