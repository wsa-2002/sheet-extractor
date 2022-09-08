import asyncio

from fastapi import APIRouter, responses, Depends, Request

import log
from middleware.headers import get_auth_token
from service.extractor import SheetExtractor
from persistence.line import LineHandler
from persistence.s3 import s3_handler
from utils import url
from utils import validators

router = APIRouter(tags=['Public'], dependencies=[Depends(get_auth_token)])


@router.post("/", status_code=200, response_class=responses.HTMLResponse)
@router.get("/", status_code=200, response_class=responses.HTMLResponse)
async def default_page():
    return "<a href=\"/docs\">/docs</a>"


@router.post("/callback")
async def callback(request: Request):
    log.info("get request")
    # signature = request.headers['X-Line-Signature']
    body = await request.body()
    reply_token = url.get_reply_token_from_request(body.decode())
    video_url = url.get_url_from_request(body.decode())
    if not validators.youtube_url(video_url):
        LineHandler.send_message(reply_token=reply_token,
                                 raw_message='Invalid url, please resend.')
    with SheetExtractor(url=video_url) as s3_file:
        sign_url = s3_handler.sign_url(bucket=s3_file.bucket, key=s3_file.key, filename=f"{s3_file.uuid}.pdf")
    LineHandler.send_message(reply_token=reply_token,
                             raw_message=sign_url)
    pass
