
def ws_add(message):

    message.reply_channel.group_send({"accept": True})

    ("chat").add(message.reply_channel)

def ws_message(message):
    ("chat").group_send({
        "text": message.content['text'],
    })

def ws_disconnect(message):
    ("chat").discard(message.reply_channel)