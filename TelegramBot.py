from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, filters, CommandHandler, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests as rq
import json
import telebot

bot = telebot.TeleBot("5456756222:AAELc-ihxQKzfnKhoMe_hHhI1P9HeW2GHmc")


def RunAPI(API):
    x = rq.get(API)
    Respone = json.loads(x.text)  # Biến đổi API trả về thành dạng dictionary.
    DetailsHash = {}  # Lưu chi tiết về một TxnHash
    apiRespone = {  # Lưu toàn bộ API trả về, nhưng được tách nhỏ để sử dụng
        'bscscan': None,
        'etherscan': {
            'erc20': [],
            'erc721': [],
            'erc1155': [],
        }
    }
    for _i in Respone:
        for __i in Respone[_i]:
            for ___i in Respone[_i][__i]:
                apiRespone['etherscan'][__i].append(___i['TxnHash'])
                DetailsHash[___i['TxnHash']] = ___i

    # apiRespone['etherscan']['amount'] = len(apiRespone['etherscan']['erc20']) + len(
    #     apiRespone['etherscan']['erc721']) + len(apiRespone['etherscan']['erc1155'])
    return apiRespone, DetailsHash


apiRespone, DetailsHash = RunAPI('https://navara.5labs.io/token/approval?address=0xb8c2c29ee19d8307cb7255e1cd9cbde883a267d5')

# từ phần này sẽ code tương tác với bot


async def Approval(update: Update) -> None:
    await update.message.reply_text("""Bscscan: 0\nEtherscan:
    - erc20: {}
    - erc721: {}
    - erc1155: {}
    """.format(len(apiRespone['etherscan']['erc20']), len(apiRespone['etherscan']['erc721']), len(apiRespone['etherscan']['erc1155'])) + 'type + index + amount to get details information of hash \n' + 'Ex: erc20 1 5')


def erc_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0] not in ['erc20', 'erc721', 'erc1155']:
        return False
    else:
        return True


@bot.message_handler(func=erc_request)
def send_erc(message):
    request = message.text.split()
    request[1] = int(request[1])
    request[2] = int(request[2])
    print(request[0])
    print(type(request[1]), type(request[2]))
    for i in range(request[1]-1, request[1]+request[2]-1):
        bot.send_message(message.chat.id, apiRespone['etherscan'][request[0]][i])


app = ApplicationBuilder().token("5456756222:AAELc-ihxQKzfnKhoMe_hHhI1P9HeW2GHmc").build()

app.add_handler(CommandHandler("approval", Approval))

# app.run_polling()
bot.polling()


