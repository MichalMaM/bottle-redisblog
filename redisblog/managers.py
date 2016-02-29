from .client import client
from .utils import force_text


class Manager(object):

    def __init__(self, model_class):
        self.model = model_class

    def get_last_objects(self, offset=0, count=10, keys=None, pipe=None):
        pipe = pipe or client.pipeline()
        keys = keys or self.model.get_keys()
        pipe.zrevrange(
            keys['order_listing'],
            start=offset,
            end=offset + count - 1,
            withscores=True
        )
        results = pipe.execute()

        for value, score in results[-1]:
            pk = int(force_text(value).rsplit('_',)[-1])
            obj = self.get_obj(pk, pipe)
            if not obj:
                # TODO: add log
                continue
            yield obj

    def get_obj(self, pk, keys_with_id=None, pipe=None):
        # TODO: check if id exists
        pipe = pipe or client.pipeline()
        keys_with_id = keys_with_id or self.model.get_keys_with_id(pk)
        pipe.hgetall(keys_with_id['attrs'])
        attrs_dict = {force_text(k): v for k, v in pipe.execute()[-1].items()}
        if not attrs_dict:
            return None
        return self.model(**attrs_dict)
