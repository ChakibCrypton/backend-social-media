import logging
from enum import Enum
from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from socialmedia_api.database import comment_table, database, like_table, post_table
from socialmedia_api.models.post import (
    Comment,
    CommentIn,
    PostLike,
    PostLikeIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
    UserPostWithLikes,
)
from socialmedia_api.models.user import User
from socialmedia_api.security import get_current_user
from socialmedia_api.tasks import generate_and_add_to_post

post_router = APIRouter()
logger = logging.getLogger(__name__)


select_post_and_likes = (
    sqlalchemy.select(post_table, sqlalchemy.func.count(like_table.c.id).label("likes"))
    .select_from(post_table.outerjoin(like_table))
    .group_by(post_table.c.id)
)


async def find_post(post_id: int):
    logger.info(f"Finding post with id {post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query)


@post_router.post("/post", response_model=UserPost, status_code=201)
async def create_post(
    post: UserPostIn,
    current_user: Annotated[User, Depends(get_current_user)],
    background_tasks: BackgroundTasks,
    request: Request,
    prompt: str = None,
):
    logger.info("Creating post ")
    data = {**post.model_dump(), "user_id": current_user.id}  # previously .dict()
    query = post_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)  # execute renvoie un id
    new_post = {**data, "id": last_record_id}

    if prompt:
        background_tasks.add_task(
            generate_and_add_to_post,
            current_user.email,
            last_record_id,
            request.url_for("get_post_with_comments", post_id=last_record_id),
            database,
            prompt,
        )

    return new_post


class PostSorting(str, Enum):
    new = "new"
    old = "old"
    most_likes = "most_likes"


@post_router.get("/post", response_model=list[UserPostWithLikes])
async def get_all_posts(
    sorting: PostSorting = PostSorting.new,
):  # sorting in ?sorting="old"
    logger.info("Getting all post")

    if sorting == PostSorting.new:
        query = select_post_and_likes.order_by(post_table.c.id.desc())
    elif sorting == PostSorting.old:
        query = select_post_and_likes.order_by(post_table.c.id.asc())
    elif sorting == PostSorting.new:
        query = select_post_and_likes.order_by(sqlalchemy.desc("likes"))

    logger.debug(query)

    return await database.fetch_all(query)


@post_router.post("/comment", response_model=Comment)
async def create_comment(
    comment: CommentIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Creating comment")

    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**comment.model_dump(), "user_id": current_user.id}
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    new_comment = {**data, "id": last_record_id}
    return new_comment


@post_router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    logger.info("Getting comments on post")

    query = comment_table.select().where(comment_table.c.post_id == post_id)

    logger.debug(query)
    return await database.fetch_all(query)


@post_router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    logger.info("Getting post and its comments")

    query = select_post_and_likes.where(post_table.c.id == post_id)

    logger.debug(query)

    post = await database.fetch_one(query)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    post_with_comments = {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
    return post_with_comments


@post_router.post("/like", response_model=PostLike, status_code=201)
async def like_post(
    like: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Adding a like")

    post = await find_post(like.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {"post_id": like.post_id, "user_id": current_user.id}
    query = like_table.insert().values(data)

    logger.debug(query)

    id_like = await database.execute(query)
    new_like = {**data, "id": id_like}
    return new_like


@post_router.get("/like/{post_id}", response_model=list[PostLike])
async def get_like(post_id: int):
    logger.info(f"Getting likes for the post {post_id}")

    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    query = like_table.select().where(like_table.c.post_id == post_id)
    logger.debug(query)

    return await database.fetch_all(query)
