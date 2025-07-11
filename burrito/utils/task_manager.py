"""
    Async manager for task management, create or get running event cycle.

"""

import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import Any

from burrito.utils.logger import get_logger
from burrito.utils.singleton_pattern import singleton


@singleton
class _TaskManager:
    def __init__(self) -> None:
        """
        Initialization event loop fot current thread
        """

        self._thread_pool = ThreadPoolExecutor(max_workers=25)
        self._loop = self._get_running_loop()

        asyncio.set_event_loop(self._loop)

    def __del__(self):
        self._thread_pool.shutdown(wait=True)

    def _get_running_loop(self) -> asyncio.AbstractEventLoop:
        """
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
            get_logger().warning("Async loop is not running...")
            return None

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """
        Return instance of asynchronous event loop

        Returns:
            asyncio.AbstractEventLoop: event loop object
        """

        return self._loop

    @property
    def pool(self) -> ThreadPoolExecutor:
        return self._thread_pool

    def add_task(self, task, *args, daemon=False, **kwargs) -> None:
        """
        Add task to execute in event loop

        Args:
            task (_type_): function/coroutine object
        """

        if inspect.iscoroutine(task):
            self._loop.create_task(task)
        else:
            if daemon:
                Thread(target=task, args=args, kwargs=kwargs, daemon=True).start()
            else:
                self._thread_pool.submit(task, *args, **kwargs)

    def add_multiply_task(self, task_list: tuple[Any]) -> None:
        """
        Create few tasks using

        Args:
            task_list (tuple[Any]): function/coroutine tuple
        """

        for task in task_list:
            self.add_task(task)

    def run(self, *, forever: bool = True) -> None:
        """
        Run current event loop forever

        Args:
            forever (bool, optional):
                If this option is True cycle run forever else until complete. Defaults to True.
        """

        if self._loop.is_running():  # exit function if loop is running
            return

        if forever:
            self._loop.run_forever()
        else:
            self._loop.run_until_complete(
                asyncio.gather(
                    *asyncio.all_tasks(self._loop)  # unpack task list
                )
            )

    def stop(self):
        """
        Stop running event loop
        """

        self._loop.stop()


def get_task_manager() -> _TaskManager:
    """
    Interface to get access to AsyncManager

    Returns:
        __TaskManager: task manager object
    """

    return _TaskManager()
