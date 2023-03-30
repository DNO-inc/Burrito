"""
    Async manager for task management, create or get running event cycle.

"""

import asyncio
import sys

from burrito.utils.singleton_pattern import singleton
from burrito.utils.logger import logger


@singleton
class __TaskManager:
    def __init__(self) -> None:
        """_summary_

            Initialization event loop fot current thread

        """

        self.__loop = self.__get_running_loop()

        asyncio.set_event_loop(self.__loop)

    def __get_running_loop(self) -> asyncio.AbstractEventLoop:
        """_summary_

        Create or return running event loop

        Returns:
            asyncio.AbstractEventLoop: event loop object
        """

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
        """_summary_

        Return instance of asynchronous event loop

        Returns:
            asyncio.AbstractEventLoop: event loop object
        """

        return self.__loop

    def add_task(self, coro) -> None:
        """_summary_

        Add task to execute in event loop

        Args:
            coro (_type_): coroutine object
        """

        self.__loop.create_task(coro)

    def run(self, *, forever: bool = True) -> None:
        """_summary_

        Run current event loop forever

        Args:
            forever (bool, optional):
                If this option is True cycle run forever else until complite. Defaults to True.
        """

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
        """_summary_

        Stop running event loop
        """

        self.__loop.stop()


def get_async_manager() -> __TaskManager:
    """_summary_

    Interface to get access to AsyncManager

    Returns:
        __TaskManager: task manager object
    """

    return __TaskManager()
