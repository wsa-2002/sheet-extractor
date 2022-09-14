from fastapi import APIRouter, responses, Depends, Request

from middleware.headers import get_auth_token
from service.extractor import SheetExtractor
from persistence.line import LineHandler
from persistence.s3 import s3_handler
from persistence import database as db
from utils import url
from utils import validators

router = APIRouter(tags=['Public'], dependencies=[Depends(get_auth_token)])


@router.post("/", status_code=200, response_class=responses.HTMLResponse)
@router.get("/", status_code=200, response_class=responses.HTMLResponse)
async def default_page():
    return "<a href=\"/docs\">/docs</a>"
