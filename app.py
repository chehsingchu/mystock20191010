#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('VbgVFJ5GcUXalkkCjKXiMVWTrmGW+r3DN9VeZozSLX+Zq4hRXcrS/wI6XPnkLMX5swDxQcjlYuXHdXRBGpdilOJ86xlcmnk8Cuo66GBAS/Wx0DfrzYZFAxbdbo5qmqIS6/Sbz5oa72D8DJ278aRkCQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('ff40e56527658634a2bbbb65cd25eee4')

line_bot_api.push_message('Ube8f42668a7d9ce94b0728af9b9205eb', TextSendMessage(text='小秘書測試'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
