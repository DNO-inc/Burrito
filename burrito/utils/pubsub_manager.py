import asyncio

from burrito.utils.logger import get_logger
from burrito.utils.singleton_pattern import singleton
from burrito.utils.redis_utils import get_redis_cursor


@singleton
class PubSubManager:
    def __init__(self) -> None:
        self.__subscriber = get_redis_cursor().pubsub()

    async def run(self):
        get_logger().info("PubSubManager is running")

        await self.__subscriber.psubscribe("*")
        while True:
            message = await self.__subscriber.get_message()
            if message:
                print(message)

            await asyncio.sleep(0.1)


def get_pubsub_manager() -> PubSubManager:
    return PubSubManager()


"""
async def pubsub():
    redis = aioredis.Redis(
        host="localhost",
        port=6379,
        password="root"
    )
    psub = redis.pubsub()

    async def reader(channel: aioredis.client.PubSub):
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        print(message)
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass

    async with psub as p:
        await p.subscribe("test_email_messages")
        await reader(p)  # wait for reader to complete
        await p.unsubscribe("test_email_messages")

    # closing all open connections
    await psub.close()


async def main():
    tsk = asyncio.create_task(pubsub())

    async def publish():
        pub = aioredis.Redis(
            host="localhost",
            port=6379,
            password="root"
        )
        while not tsk.done():
            # wait for clients to subscribe
            # publish some messages
            for msg in ["one", "two", "three"]:
                print(f"(Publisher) Publishing Message: {msg}")
                await pub.publish("channel:1", msg)
        await pub.close()

    await publish()
"""


#if __name__ == "__main__":
#    import os

#    if "redis_version:2.6" not in os.environ.get("REDIS_VERSION", ""):
#        asyncio.run(main())
