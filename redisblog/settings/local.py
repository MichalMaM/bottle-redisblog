from os.path import exists, join
from .base import DEV_TMP_DIR

# check tmp directory exists or create
if not exists(DEV_TMP_DIR):
    from os import makedirs
    makedirs(DEV_TMP_DIR)

