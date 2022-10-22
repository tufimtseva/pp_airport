from waitress import serve
import airportapp
serve(airportapp.app, host='127.0.0.1', port=5000)