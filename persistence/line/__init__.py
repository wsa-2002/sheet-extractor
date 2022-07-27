from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from config import line_config


class LineHandler:
    line_bot_api = LineBotApi(line_config.channel_access_token)
    parser = WebhookParser(line_config.channel_secret)
    handler = WebhookHandler(line_config.channel_secret)

    @staticmethod
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event: MessageEvent):
        reply_token = event.reply_token

        if isinstance(event.message, TextMessage):
            LineHandler.send_message(reply_token=reply_token, raw_message=event.message.text)

    @classmethod
    def send_message(cls, reply_token: str, raw_message: str):
        messages = TextSendMessage(text=raw_message)
        cls.line_bot_api.reply_message(reply_token=reply_token, messages=messages)
