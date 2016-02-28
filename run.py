from bottle import run
from redisblog.app import app

run(app, host='0.0.0.0', port=8080)
