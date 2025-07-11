from fastapi import HTTPException

from burrito.models.faculty_model import Faculties
from burrito.models.group_model import Groups
from burrito.models.queues_model import Queues
from burrito.models.statuses_model import Statuses


def _raise_converter_error(detail) -> None:
    raise HTTPException(
        status_code=422,
        detail=detail
    )


class Converter:
    @staticmethod
    def _is_empty(int_value: int | None, error_detail: str = "") -> None:
        if not isinstance(int_value, int) or int_value <= 0:
            _raise_converter_error(error_detail)

    @staticmethod
    def convert(int_value: int | None):
        raise NotImplementedError("This is an abstract method")


class GroupConverter(Converter):
    @staticmethod
    def convert(int_value: int | None) -> Groups | None:
        """
        Args:
            int_value (int): group id

        Returns:
            Groups | None: group object or None value
        """
        GroupConverter._is_empty(int_value, f"Group {int_value} is invalid")

        group_object = Groups.get_or_none(Groups.group_id == int_value)
        if not group_object:
            _raise_converter_error(f"Group {int_value} is not found")

        return group_object


class FacultyConverter(Converter):
    @staticmethod
    def convert(int_value: int | None) -> Faculties | None:
        """
        Args:
            int_value (int): faculty id

        Returns:
            Faculties | None: faculty object or None value
        """
        FacultyConverter._is_empty(int_value, f"Faculty {int_value} is invalid")

        faculty_object = Faculties.get_or_none(Faculties.faculty_id == int_value)
        if not faculty_object:
            _raise_converter_error(f"Faculty {int_value} is not found")

        return faculty_object


class QueueConverter(Converter):
    @staticmethod
    def convert(int_value: int | None) -> Queues | None:
        """
        Args:
            int_value (int): queue id

        Returns:
            Queues | None: queue object or None value
        """

        # INFO: queue value can be None
        if int_value is None:
            return None

        QueueConverter._is_empty(int_value, f"Queue {int_value} is invalid")

        queue_object = Queues.get_or_none(Queues.queue_id == int_value)
        if not queue_object:
            _raise_converter_error(f"Queue {int_value} is not found")

        return queue_object


class StatusConverter(Converter):
    @staticmethod
    def convert(int_value: int | None) -> Statuses | None:
        """
        Args:
            int_value (int): 'status' id

        Returns:
            Statuses | None: 'status' object or None value
        """
        StatusConverter._is_empty(int_value, "Status is invalid")

        status_object = Statuses.get_or_none(Statuses.status_id == int_value)
        if not status_object:
            _raise_converter_error("Status is invalid")

        return status_object
