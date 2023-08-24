# -*- coding: utf-8 -*-
import time
from main import main, templates, config
from fastapi import Request, status, HTTPException
from fastapi.exceptions import ValidationException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from main.models.database import query_execute
from main.api.api_auth import update_token
from main.utils.user import get_user_by_token_with_type


@main.exception_handler(ValidationException)
async def validation_exeption_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


@main.middleware("http")
async def before_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@main.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@main.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("test.html", context={"request": request})
