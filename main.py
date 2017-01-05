import json
import re
from flask import Flask, request, url_for
import config
import bot_wrapper
from google_calendar_wrapper import GoogleCalendarWrapper

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    return "Use '/bothook' url as Telegram API webhook target."


@app.route('/bothook', methods=['POST'])
def bot_hook():
    if request.method == 'POST' and request.is_json:
        bot_wrapper.process_updates(request.get_json())
        return 'ok'


@app.route('/resethook', methods=['POST'])
def reset_hook():
    if request.method == 'POST':
        result = bot_wrapper.reset_webhook()
        return json.dumps(result)


@app.route('/authendpoint')
def auth_endpoint():

    # 'state' argument was set to user id on first step of auth2 flow
    user_id = request.args.get('state')

    auth_code = request.args.get('code')
    redirect_url = reverse('auth_endpoint')
    calendar_wrapper = GoogleCalendarWrapper(user_id, redirect_url)
    calendar_wrapper.update_credentials(auth_code)
    return 'Thank you. Authorization granted, you can close this page now.'


def reverse(func_name, scheme='https', external=True):
    with app.test_request_context():
        url = url_for(func_name, _external=external, _scheme=scheme)

        # SERVER_NAME for debug server can be different from public server
        if 'FAKE_SERVER_NAME' in app.config:
            url = re.sub(
                r'://.+/',
                '://{}/'.format(app.config['FAKE_SERVER_NAME']),
                url
            )
        return url

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        ssl_context=app.config['SSL_CONTEXT'],
    )
