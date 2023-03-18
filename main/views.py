# -*- coding: utf-8 -*-
from main import main, templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from main.models.database import Session, User


@main.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # with Session() as db:
    #     print(db.query(User).all())
    return templates.TemplateResponse("index.html", context={"request": request})


# @main.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("login"))
