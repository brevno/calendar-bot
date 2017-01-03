import json
from flask import request
from app import app
import bot_wrapper


@app.route('/')
def hello_world():
    return "Use '/bothook' url as Telegram API webhook target."


@app.route('/bothook', methods=['POST'])
def bot_hook():
    if request.method == 'POST' and request.is_json:
        print('in hook')
        bot_wrapper.process_updates(request.get_json())
        return json.dumps(True)


@app.route('/resethook', methods=['POST'])
def reset_hook():
    if request.method == 'POST':
        result = bot_wrapper.reset_webhook()
        return json.dumps(result)

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        ssl_context=app.config['SSL_CONTEXT'],
    )
