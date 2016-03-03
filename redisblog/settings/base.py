from os.path import join, dirname, pardir, abspath

PROJECT_ROOT = abspath(join(dirname(__file__), pardir))
DEV_TMP_DIR = join(PROJECT_ROOT, pardir, '.devtmp')

PROJECT_PREFIX = 'redisblog'

STATIC_URL = '/static/'
STATIC_ROOT = join(PROJECT_ROOT, 'redisblog', 'static')

URL_PREFIXES = {
    'article': '/article',
}

URLS_MAPPING = {
    'hp': '/',
    'article_add': '/add/',
    'article_edit': '/edit/<pk:int>/',
    'article_add_success': '/add/success/',
    'article_detail': '/<pk:int>',
    'article_delete': '/delete/<pk:int>',
    'article_delete_success': '/delete/success/',
}

FULL_URLS_MAPPING = {}

for key, val in URLS_MAPPING.items():
    key_prefix = key.split('_')[0]
    if key_prefix in URL_PREFIXES:
        val = '%s%s' % (URL_PREFIXES[key_prefix], val)
    FULL_URLS_MAPPING[key] = val


REDIS_BACKEND = {
    'host': 'localhost',  # XXX: change in production
    'port': 6379,  # XXX: change in production
    'db': 13,
}
