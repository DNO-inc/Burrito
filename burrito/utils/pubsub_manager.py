import asyncio
from typing import Any
from inspect import iscoroutinefunction

from burrito.utils.logger import get_logger
from burrito.utils.singleton_pattern import singleton
from burrito.utils.redis_utils import get_redis_cursor


@singleton
class PubSubManager:
    def __init__(self) -> None:
        self.__subscriber = get_redis_cursor().pubsub()
        self.__callbacks: dict[str, Any] = {}

    def add_callback(self, chanel: str, callback) -> None:
        """_summary_

        Add back functions

        Args:
            chanel (str): chanel name
            callback (function): callable functions
        """

        if self.__callbacks.get(chanel):
            get_logger().critical("Callback with the same name exist")
            return

        self.__callbacks[chanel] = callback

    async def run(self) -> None:
        """_summary_

        Run PubSub cycle
        """

        get_logger().info("PubSubManager is running")

        await self.__subscriber.psubscribe("*")
        while True:
            message = await self.__subscriber.get_message()
            channel = None
            data = None
            callback = None

            if message:
                channel = message.get("channel").decode("utf-8")
                data = message.get("data")
                if isinstance(data, bytes):
                    data = data.decode("utf-8")

                callback = self.__callbacks.get(channel)
                if callback:
                    if iscoroutinefunction(callback):
                        await callback()
                    else:
                        callback()

                    print(channel, data)

            await asyncio.sleep(0.1)


def get_pubsub_manager() -> PubSubManager:
    return PubSubManager()
