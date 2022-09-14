from fastapi import APIRouter, Request

from service.extractor import SheetExtractor
from persistence.line import LineHandler
from persistence.s3 import s3_handler
from persistence import database as db
from utils import url
from utils import validators

router = APIRouter(tags=['Line'])


@router.post("/callback")
async def callback(request: Request):
    body = await request.body()
    reply_token = url.get_reply_token_from_request(body.decode())

    if not reply_token:
        return

    video_url = url.get_url_from_request(body.decode())
    if not validators.youtube_url(video_url):
        LineHandler.send_message(reply_token=reply_token,
                                 raw_message='Invalid url, please resend.')

    sheet = await db.sheet.get(url=video_url)
    if sheet:
        s3_file = await db.s3_file.get(s3_file_uuid=sheet.s3_file_uuid)
        sign_url = s3_handler.sign_url(bucket=s3_file.bucket, key=s3_file.key, filename=f"{s3_file.uuid}.pdf")
    else:
        with SheetExtractor(url=video_url) as s3_file:
            await db.s3_file.add(s3_file=s3_file)
            await db.sheet.add(url=video_url, s3_file_uuid=s3_file.uuid)
            sign_url = s3_handler.sign_url(bucket=s3_file.bucket, key=s3_file.key, filename=f"{s3_file.uuid}.pdf")

    LineHandler.send_message(reply_token=reply_token,
                             raw_message=sign_url)
