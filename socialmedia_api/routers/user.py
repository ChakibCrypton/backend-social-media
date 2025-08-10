import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from socialmedia_api import tasks
from socialmedia_api.database import database, user_table
from socialmedia_api.models.user import UserIn
from socialmedia_api.security import (
    authenticate_user,
    create_access_token,
    create_confirmation_token,
    get_password_hash,
    get_subject_for_token_type,
    get_user,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn, background_tasks: BackgroundTasks, request: Request):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists",
        )

    # VERY BAD IDEA NEVER STORE PASSWORD IN PLAIN TEXT
    hash_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hash_password)

    logger.debug(query)
    await database.execute(query)
    background_tasks.add_task(
        tasks.send_user_registration_email,
        user.email,
        confirmation_url=request.url_for(
            "confirm_email", token=create_confirmation_token(user.email)
        ),
    )

    return {"detail": "User created. Please confirm your email."}


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirm/{token}")  # No in the authorization header here
async def confirm_email(token: str) -> dict:
    logger.info("Confirmation of the user's email")

    email = get_subject_for_token_type(token, "confirmation")

    query = (
        user_table.update().where(user_table.c.email == email).values(confirmed=True)
    )
    logger.debug(query)

    await database.execute(query)
    return {"detail": "User confirmed"}
