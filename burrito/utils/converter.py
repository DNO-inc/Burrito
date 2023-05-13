from burrito.models.group_model import Groups
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues
from burrito.models.statuses_model import Statuses


class Converter:
    @staticmethod
    def convert(str_value: str):
        raise NotImplementedError("This is an abstract method")


class GroupStrToInt(Converter):
    @staticmethod
    def convert(str_value: str) -> Groups | None:
        """_summary_

        Args:
            str_value (str): group name

        Returns:
            Groups | None: group object or None value
        """

        return Groups.get_or_none(Groups.name == str_value)


class FacultyStrToInt(Converter):
    @staticmethod
    def convert(str_value: str) -> Faculties | None:
        """_summary_

        Args:
            str_value (str): faculty name

        Returns:
            Faculties | None: faculty object or None value
        """

        return Faculties.get_or_none(Faculties.name == str_value)


class QueueStrToInt(Converter):
    @staticmethod
    def convert(str_value: str) -> Queues | None:
        """_summary_

        Args:
            str_value (str): queue name

        Returns:
            Queues | None: queue object or None value
        """

        return Queues.get_or_none(Queues.name == str_value)


class StatusStrToInt(Converter):
    @staticmethod
    def convert(str_value: str) -> Statuses | None:
        """_summary_

        Args:
            str_value (str): 'status' name

        Returns:
            Statuses | None: 'status' object or None value
        """

        return Statuses.get_or_none(Statuses.name == str_value)
