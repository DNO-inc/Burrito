"""
    Async manager for task management

"""

import asyncio
import sys

from burrito.utils.singleton_pattern import singleton
from burrito.utils.logger import logger


@singleton
class __TaskManager:
    def __init__(self) -> None:
        self.__loop = self.__get_running_loop()

        asyncio.set_event_loop(self.__loop)

    def __get_running_loop(self) -> asyncio.AbstractEventLoop:
        """Create or return running event loop"""

        try:
            return asyncio.get_running_loop()

        except RuntimeError:
            return asyncio.new_event_loop()

        except Exception as e:
            logger.critical(f"Unexpected error {e}")
            logger.info("Exit program")
            sys.exit(1)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Return instance of asynchronous event loop"""

        return self.__loop

    def add_task(self, coro) -> None:
        """Add task to execute in event loop"""

        self.__loop.create_task(coro)

    def run(self, *, forever: bool = True) -> None:
        """Run current event loop forever"""

        if self.__loop.is_running:  # exit function if loop is running
            return

        if forever:
            self.__loop.run_forever()
        else:
            self.__loop.run_until_complete(
                asyncio.gather(
                    *asyncio.all_tasks(self.__loop)  # unpack task list
                )
            )

    def stop(self):
        """Stop running event loop"""

        self.__loop.stop()


def get_async_manager() -> __TaskManager:
    """Interface to get access to AsyncManager"""

    return __TaskManager()
