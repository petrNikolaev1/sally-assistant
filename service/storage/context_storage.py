from typing import List

from aioredis import Redis

from service.constants import INITIAL_PROMPT
from service.storage.context import UserContext


class Storage:
    def __init__(self, storage: Redis):
        self.storage = storage

    async def get_context(self, user_id: str) -> UserContext:
        context = await self.storage.get(user_id)
        return UserContext.from_json(context)

    async def update_context(self, user_id: str, context: UserContext) -> None:
        await self.storage.set(user_id, context.to_json())

    async def reset_context(self, user_id: str) -> None:
        await self.storage.set(
            name=user_id,
            value=UserContext(
                chat_context=[INITIAL_PROMPT]
            ).to_json()
        )

    async def save_template(self, user_id: str, name: str, template: str) -> None:
        await self.storage.set(f"{user_id}:templates:{name}", template)

    async def delete_template(self, user_id: str, name: str) -> None:
        await self.storage.delete(f"{user_id}:templates:{name}")

    async def get_template(self, user_id: str, name: str) -> str:
        resp = await self.storage.get(f"{user_id}:templates:{name}")
        return resp.decode()

    async def list_templates(self, user_id: str) -> List[str]:
        return [name.decode().split(":")[-1] for name in await self.storage.keys(f"{user_id}:templates:*")]
