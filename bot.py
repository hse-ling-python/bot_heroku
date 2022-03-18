import flask
import telebot
import os

TOKEN = os.environ["TOKEN"]


bot = telebot.TeleBot(TOKEN, threaded=False)


# bot.remove_webhook()
bot.set_webhook(url="https://stark-garden-80398.herokuapp.com/bot")

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает длину вашего сообщения.")


@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует все прочие сообщения
def send_len(message):
    bot.send_message(message.chat.id, 'В вашем сообщении {} символов.'.format(len(message.text)))

@app.route("/", methods=['GET', 'HEAD'])
def index():
    return 'ok'

# страница для нашего бота
@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
    
if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

