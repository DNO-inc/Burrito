from queue import Queue
from time import sleep as init_sleep

from burrito.init.init_task import InitTask

from burrito.utils.logger import get_logger


class InitManager:
    def __init__(self, error_attempt_delta: int = 3) -> None:
        self.__init_tasks: Queue = Queue()
        self.__error_attempt_delta = error_attempt_delta
        self.__error_count = 0
        self.__critical_error_count = 0

    @property
    def errors(self) -> int:
        return self.__error_count

    @property
    def critical(self) -> int:
        return self.__critical_error_count

    def add_task(self, task: InitTask):
        self.__init_tasks.put(task)

    def run_cycle(self):
        while not self.__init_tasks.empty():
            task: InitTask = self.__init_tasks.get()

            get_logger().info(f"Run task\t'{task.__class__.__name__}'")

            if issubclass(task.__class__, InitTask):
                attempts_remain = task.attempt_count

                while attempts_remain > 0:
                    if task._run_task():
                        break

                    get_logger().error(f"Error in task\t'{task.__class__.__name__}'")
                    init_sleep(self.__error_attempt_delta)

                    attempts_remain -= 1

                if attempts_remain <= 0:
                    self.__error_count += 1
