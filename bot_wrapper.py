from dateutil.parser import parse as date_parse
import telebot
import config
from google_calendar_wrapper import GoogleCalendarWrapper


bot_instance = telebot.TeleBot(config.BOT_TOKEN)


def reset_webhook():
    from main import reverse
    bot_instance.remove_webhook()
    return bot_instance.set_webhook(
        url=reverse('bothook'),
        certificate=open(config.SSL_CONTEXT[0], 'r')
    )


@bot_instance.message_handler(commands=['list'])
def list_events(msg):
    from main import reverse
    redirect_url = reverse('auth_endpoint')

    calendar_wrapper = GoogleCalendarWrapper(msg.from_user.id, redirect_url)
    events = calendar_wrapper.get_events_list()
    if 'status' in events \
            and events['status'] == 'error' \
            and events['error'] == 'invalidCredentials':

        authorization_url = calendar_wrapper.get_authorization_url()
        # FIXME: This exposes webhook host and oauth2 endpoint handler.
        # FIXME: Not sure this is the best thing to do.
        bot_instance.send_message(
            msg.chat.id,
            'This bot is not authorized to read your calendar. '
            'You can set credentials for bot by following this link: '
            '{}'.format(authorization_url)
        )
    else:
        reply_text = ''
        for event in events['items']:
            time = date_parse(event['start']['dateTime'])
            time_str = time.strftime('%d %h %Y %H:%M')
            event_line = '{} - {}\n'.format(time_str, event['summary'])
            reply_text += event_line
        bot_instance.send_message(msg.chat.id, reply_text)


@bot_instance.message_handler()
def reply_with_name(msg):
    bot_instance.reply_to(
        msg,
        'user {} said {}'.format(msg.from_user.first_name, msg.text)
    )


def process_updates(json_string):
    updates = [telebot.types.Update.de_json(json_string)]
    return bot_instance.process_new_updates(updates)


__all__ = 'reset_webhook, process_updates'
