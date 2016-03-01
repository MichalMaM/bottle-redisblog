from os.path import join, dirname, pardir, abspath

PROJECT_ROOT = abspath(join(dirname(__file__), pardir))
DEV_TMP_DIR = join(PROJECT_ROOT, pardir, '.devtmp')

STATIC_URL = '/static/'
STATIC_ROOT = join(PROJECT_ROOT, 'redisblog', 'static')

URLS_MAPPING = {
    'hp': '/',
    'article_add': '/article/add/',
    'article_edit': '/article/edit/<pk:int>/',
    'article_add_success': '/article/add/success/',
    'article_detail': '/article/<pk:int>',
    'article_delete': '/article/delete/<pk:int>',
    'article_delete_success': '/article/delete/success/',
}

REDIS_BACKEND = {
    'host': 'localhost',  # XXX: change in production
    'port': 6379,  # XXX: change in production
    'db': 13,
}
