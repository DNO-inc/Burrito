from burrito.models.group_model import Groups
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues
from burrito.models.statuses_model import Statuses


class Converter:
    @staticmethod
    def _is_empty(str_value: str | None) -> bool:
        return not bool(str_value)

    @staticmethod
    def convert(str_value: str | None):
        raise NotImplementedError("This is an abstract method")


class GroupStrToInt(Converter):
    @staticmethod
    def convert(str_value: str | None) -> Groups | None:
        """_summary_

        Args:
            str_value (str): group name

        Returns:
            Groups | None: group object or None value
        """

        if GroupStrToInt._is_empty(str_value):
            return None

        return Groups.get_or_none(Groups.name == str_value)


class FacultyStrToInt(Converter):
    @staticmethod
    def convert(str_value: str | None) -> Faculties | None:
        """_summary_

        Args:
            str_value (str): faculty name

        Returns:
            Faculties | None: faculty object or None value
        """

        if FacultyStrToInt._is_empty(str_value):
            return None

        return Faculties.get_or_none(Faculties.name == str_value)


class QueueStrToInt(Converter):
    @staticmethod
    def convert(str_value: str | None) -> Queues | None:
        """_summary_

        Args:
            str_value (str): queue name

        Returns:
            Queues | None: queue object or None value
        """

        if QueueStrToInt._is_empty(str_value):
            return None

        return Queues.get_or_none(Queues.name == str_value)


class StatusStrToInt(Converter):
    @staticmethod
    def convert(str_value: str | None) -> Statuses | None:
        """_summary_

        Args:
            str_value (str): 'status' name

        Returns:
            Statuses | None: 'status' object or None value
        """

        if StatusStrToInt._is_empty(str_value):
            return None

        return Statuses.get_or_none(Statuses.name == str_value)
