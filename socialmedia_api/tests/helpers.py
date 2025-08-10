from httpx import AsyncClient


# ✅ Fonction utilitaire pour créer un post
async def create_post(
    body: str, async_client: AsyncClient, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_comment(
    async_client: AsyncClient, post_id: int, body: str, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/comment",
        json={"post_id": post_id, "body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def like_post(
    async_client: AsyncClient, post_id: int, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/like",
        json={"post_id": post_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()
