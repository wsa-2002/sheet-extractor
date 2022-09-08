import json


def get_url_from_request(request: str):
    request = json.loads(request)
    print(request['events'])
    return request['events'][0]['message']['text']


def get_reply_token_from_request(request: str):
    request = json.loads(request)
    return request['events'][0]['replyToken']
