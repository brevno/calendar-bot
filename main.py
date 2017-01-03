from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(port=8080, ssl_context=context)
