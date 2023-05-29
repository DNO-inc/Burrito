from peewee import Model, ModelBase

from burrito.utils.singleton_pattern import singleton

from burrito.mm.exceptions import (
    ObjectIsNotModelError,
    PaginationValueError,
    InvalidFilterError
)


@singleton
class ModelManager:
    def __init__(self, *, models: list[Model] | None = None) -> None:
        self.__models = models if models is not None else []

    @property
    def models(self) -> list[Model]:
        return self.__models

    def add_model(self, model: Model) -> None:
        is_valid_model = False
        for parent_class in model.__class__.__mro__:
            if issubclass(parent_class, ModelBase):
                is_valid_model = True
                self.__models.append(model)
                break

        if not is_valid_model:
            raise ObjectIsNotModelError(
                f"This class {model.__class__} is not subclass of Model"
            )

    def add_models(self, models: list[Model]) -> None:
        for model in models:
            self.add_model(model)

    def select_all(
        self,
        model: Model,
        *,
        sort_by: list = None,
        page_start: int = 0,
        items_count: int = 10
    ) -> list[Model]:
        if page_start < 0:
            raise PaginationValueError(
                f"Start page values is invalid: {page_start}"
            )

        if items_count < 0:
            raise PaginationValueError(
                f"items count per page is invalid: {items_count}"
            )

        if sort_by:
            return [
                item for item in model.select().order_by(sort_by).paginate(
                    page_start,
                    items_count
                )
            ]

        return [
            item for item in model.select().paginate(
                page_start,
                items_count
            )
        ]

    def select_by_filter(
        self,
        model,
        *,
        _filters: list | tuple | set,
        sort_by: list = None,
        page_start: int = 0,
        items_count: int = 10
    ) -> list[Model]:
        if not isinstance(_filters, (list, tuple, set)):
            raise InvalidFilterError(f"Invalid filters detected: {_filters}")

        if not _filters:
            raise InvalidFilterError(f"Invalid filters detected: {_filters}")

        if page_start < 0:
            raise PaginationValueError(
                f"Start page values is invalid: {page_start}"
            )

        if items_count < 0:
            raise PaginationValueError(
                f"items count per page is invalid: {items_count}"
            )

        if sort_by:
            return [
                item for item in model.select().where(
                    *_filters
                ).order_by(sort_by).paginate(
                    page_start,
                    items_count
                )
            ]

        return [
            item for item in model.select().where(*_filters).paginate(
                page_start,
                items_count
            )
        ]

    def update_by_filet(self, model, filters: list):
        ...

    def delete_by_filter(self, model, filters: list):
        ...


def get_model_manager() -> ModelManager:
    return ModelManager()
