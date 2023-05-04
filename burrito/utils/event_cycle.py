class __BurritoEventCycle:
    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self):
        return self.__name


class EventCycleManager:
    def __init__(self) -> None:
        self.__event_cycles: dict[str, __BurritoEventCycle] = []

    @property
    def event_cycles(self) -> dict[str, __BurritoEventCycle]:
        return self.__event_cycles

    def new_event_cycle(self, name: str):
        if self.__event_cycles.get(name):
            return

        self.__event_cycles[name] = __BurritoEventCycle(name)
