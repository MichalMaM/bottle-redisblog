from .settings import URLS_MAPPING, STATIC_URL

BASE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'urls': URLS_MAPPING
}


def add_base_context(base_context=None):
    """
    Added base variables to template context
    """
    def wrapped_decorator(func):
        def wrapped_func(*args, **kwargs):
            context = base_context or BASE_CONTEXT
            data = func(*args, **kwargs)
            final_data = context.copy()
            final_data.update(data)
            return final_data

        wrapped_func.__dict__ = func.__dict__
        wrapped_func.__doc__ = func.__doc__
        wrapped_func.__name__ = func.__name__

        return wrapped_func
    return wrapped_decorator