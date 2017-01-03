import telebot
import config


bot_instance = telebot.TeleBot(config.BOT_TOKEN)


def reset_webhook():
    bot_instance.remove_webhook()
    return bot_instance.set_webhook(
        url='https://62.109.17.97:8443/bothook',
        certificate=open(config.SSL_CONTEXT[0], 'r')
    )


@bot_instance.message_handler()
def reply_with_id(msg):
    bot_instance.reply_to(
        msg,
        'user {} said {}'.format(msg.from_user.first_name, msg.text)
    )


def process_updates(json_string):
    updates = [telebot.types.Update.de_json(json_string)]
    bot_instance.process_new_updates(updates)


__all__ = 'reset_webhook, process_updates'
