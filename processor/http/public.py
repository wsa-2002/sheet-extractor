import log

from fastapi import APIRouter, responses, Depends, Request

from middleware.headers import get_auth_token
from persistence.line import LineHandler

router = APIRouter(tags=['Public'], dependencies=[Depends(get_auth_token)])


@router.post("/", status_code=200, response_class=responses.HTMLResponse)
@router.get("/", status_code=200, response_class=responses.HTMLResponse)
async def default_page():
    return "<a href=\"/docs\">/docs</a>"


@router.post("/callback")
async def callback(request: Request):
    log.info("get request")
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    LineHandler.handler.handle(body=body.decode(), signature=signature)
    pass
