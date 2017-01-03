import config
from app import app

app.config.from_object(config)


@app.route('/')
def hello_world():
    return "Use '/bothook' url as Telegram API webhook target."


if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        ssl_context=app.config['SSL_CONTEXT'],
    )
