from waitress import serve
from init import app
import api.controller


serve(app, host='127.0.0.1', port=5000)