from burrito.utils.logger import get_logger


class InitTask:
    def __init__(
            self,
            wait_time: int = 30,
            attempt_count: int = 2,
            can_skip: bool = False,
    ) -> None:
        self.__wait_time = wait_time if wait_time >= 1 else 30
        self.__attempt_count = attempt_count if attempt_count >= 1 else 1
        self.__can_skip = can_skip if isinstance(can_skip, bool) else bool(can_skip)

    @property
    def wait_time(self) -> int:
        return self.__wait_time

    @property
    def attempt_count(self) -> int:
        return self.__attempt_count

    @property
    def can_skip(self) -> bool:
        return self.__can_skip

    def _run_task(self) -> bool | None:
        try:
            self.run()
            return True
        except Exception as exc:
            get_logger().error(exc)
            return None

    def run(self):
        raise NotImplementedError("You can't call method of abstract class")
