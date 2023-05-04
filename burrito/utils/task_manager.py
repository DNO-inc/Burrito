"""
    Async manager for task management, create or get running event cycle.

"""

from threading import get_native_id
from typing import Any
import asyncio
import sys

from burrito.utils.logger import get_logger


def thread_singleton(class_) -> Any:
    class_instance: dict[int, __TaskManager] = {}

    def get_class_instance(*args, **kwargs):
        instance_key = (class_, get_native_id())

        if not class_instance.get(instance_key):
            class_instance[instance_key] = class_(*args, **kwargs)

        return class_instance[instance_key]

    return get_class_instance


@thread_singleton
class _TaskManager:
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
            get_logger().critical(f"Unexpected error {e}")
            get_logger().info("Exit program")
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

    def add_multiply_task(self, coro_list: tuple[Any]) -> None:
        """_summary_

        Create few tasks using

        Args:
            coro_list (tuple[Any]): coroutines tuple
        """

        for coro in coro_list:
            self.add_task(coro)

    def run(self, *, forever: bool = True) -> None:
        """_summary_

        Run current event loop forever

        Args:
            forever (bool, optional):
                If this option is True cycle run forever else until complete. Defaults to True.
        """

        if self.__loop.is_running():  # exit function if loop is running
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


def get_async_manager() -> _TaskManager:
    """_summary_

    Interface to get access to AsyncManager

    Returns:
        __TaskManager: task manager object
    """

    return _TaskManager()
