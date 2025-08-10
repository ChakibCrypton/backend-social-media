import pytest
from httpx import AsyncClient

from socialmedia_api import security
from socialmedia_api.tests.helpers import create_comment, create_post, like_post


@pytest.fixture()
def mock_generate_cute_creature_api(mocker):
    return mocker.patch(
        "socialmedia_api.tasks._generate_cute_creature_api",
        return_value={"output_url": "http://example.net/image.jpg"},
    )


# ✅ Test création normale d’un post
@pytest.mark.anyio("asyncio")
async def test_create_post(
    async_client: AsyncClient, confirmed_user: dict, logged_in_token: str
):
    body = "Test post"
    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {
        "id": 1,
        "body": body,
        "user_id": confirmed_user["id"],
        "image_url": None,
    }.items() <= response.json().items()


@pytest.mark.anyio("asyncio")
async def test_create_post_with_prompt(
    async_client: AsyncClient,
    confirmed_user: dict,
    logged_in_token: str,
    mock_generate_cute_creature_api,
):
    body = "Test Post"

    response = await async_client.post(
        "/post?prompt=A cat",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert (
        {
            "id": 1,
            "body": body,
            "user_id": confirmed_user["id"],
            "image_url": None,  # We don't get the url with the response but in the get_post...
        }.items()
        <= response.json().items()
    )

    assert response.status_code == 201

    mock_generate_cute_creature_api.assert_called()


# ✅ Test erreur si champ manquant
@pytest.mark.anyio("asyncio")
async def test_create_post_missing_data(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/post",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio("asyncio")
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")
    assert response.status_code == 200
    print("EXPECTED:", created_post)
    print("ACTUAL:", response.json())

    assert created_post.items() <= response.json()[0].items()


@pytest.mark.anyio("asyncio")
@pytest.mark.parametrize("sorting, expected_order", [("new", [2, 1]), ("old", [1, 2])])
async def test_get_all_posts_sorting(
    async_client: AsyncClient,
    logged_in_token: str,
    sorting: str,
    expected_order: list[int],
):
    await create_post("Test Post 1", async_client, logged_in_token)
    await create_post("Test Post 2", async_client, logged_in_token)
    response = await async_client.get("/post", params={"sorting": sorting})

    data = response.json()
    post_ids = [post["id"] for post in data]

    assert response.status_code == 200
    assert post_ids == expected_order


# ------------------TEST COMMENT----------------------------


@pytest.fixture
async def created_comment(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    return await create_comment(async_client, 1, "First comment !", logged_in_token)


@pytest.mark.anyio("asyncio")
async def test_create_comment(
    async_client: AsyncClient,
    created_post: dict,
    confirmed_user: dict,
    logged_in_token: str,
):
    body = {"post_id": created_post["id"], "body": "Voici mon premier commentaire !"}
    response = await async_client.post(
        "/comment",
        json=body,
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 200
    assert {
        "id": 1,
        **body,
        "user_id": confirmed_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio("asyncio")
async def test_get_comment_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    assert [created_comment] <= response.json()


@pytest.mark.anyio("asyncio")
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post, created_comment
):
    response = await async_client.get(f"/post/{created_post['id']}")
    assert response.status_code == 200
    assert {
        "post": {**created_post, "likes": 0},
        "comments": [created_comment],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_missing_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get("/post/2")
    assert response.status_code == 404


@pytest.mark.anyio("asyncio")
async def test_create_post_expired_token(
    async_client: AsyncClient, confirmed_user: dict, mocker
):
    mocker.patch(
        "socialmedia_api.security.access_token_expire_minutes", return_value=-1
    )
    token = security.create_access_token(confirmed_user["email"])
    response = await async_client.post(
        "/post",
        json={"body": "Test Post"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


# ------------------TEST LIKE----------------------------


@pytest.fixture
async def created_like(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
) -> dict:
    return await like_post(async_client, 1, logged_in_token)


@pytest.mark.anyio("asyncio")
async def test_like_post(
    async_client: AsyncClient,
    confirmed_user: dict,
    created_post: dict,
    logged_in_token: str,
):
    body = {"post_id": created_post["id"]}
    response = await async_client.post(
        "/like",
        json=body,
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {
        "post_id": created_post["id"],
        "user_id": confirmed_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio("asyncio")
async def test_get_likes(
    async_client: AsyncClient, created_like: dict, registered_user: dict
):
    post_id = created_like["post_id"]
    response = await async_client.get(f"/like/{post_id}")

    assert response.status_code == 200
    assert {
        "post_id": post_id,
        "user_id": registered_user["id"],
    }.items() <= response.json()[0].items()
