from waitress import serve

from init import app

serve(app, host='127.0.0.1', port=5000)
