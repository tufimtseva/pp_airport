from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Home page '


@app.route('/api/v1/hello-world-<val>')
def hello_world(val):
    return 'Hello World ' + val, 200


if __name__ == '__main__':
    app.run()
