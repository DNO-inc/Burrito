import json
import os

from playhouse.shortcuts import model_to_dict

from burrito.models.group_model import Groups
from burrito.models.statuses_model import Statuses
from burrito.models.faculty_model import Faculties
from burrito.models.queues_model import Queues
from burrito.models.permissions_model import Permissions
from burrito.models.roles_model import Roles
from burrito.models.role_permissions_model import RolePermissions

from .logger import get_logger


class SourceIsNotDefinedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SourceIsNotAvailableError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DefaultDataBasePreprocessor:
    def __init__(self, config: dict) -> None:
        self._config = config

    @property
    def config(self):
        return self._config

    def load_data(self) -> str:
        ...

    def apply_data(self) -> None:
        ...


class CloudDataBasePreprocessor(DefaultDataBasePreprocessor):
    ...


class LocalDataBasePreprocessor(DefaultDataBasePreprocessor):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        get_logger().info("Database preprocessor is started")

    def load_data(self) -> str:
        filename = self.config.get("filename")

        if not filename:
            raise SourceIsNotDefinedError(f"filename value is '{filename}'")

        if not os.path.exists(filename):
            raise SourceIsNotAvailableError(f"File {filename} is not exist")

        with open(filename, "r", encoding="UTF-8") as file:
            return json.loads(file.read())

    def apply_data(self) -> None:
        json_data = self.load_data()

        model_keys = {
            "groups": Groups,
            "faculties": Faculties,
            "statuses": Statuses,
            "queues": Queues,
            "permissions": Permissions,
            "roles": Roles,
            "role_permissions": RolePermissions
        }

        for key in json_data:
            __model_object = model_keys.get(key)

            if not __model_object:
                continue

            data_in_config = json_data.get(key)
            data_in_db = [model_to_dict(i) for i in __model_object.select().execute()]

            print(data_in_config)
            print(data_in_db)
            print("\n\n")

            for note in data_in_config:
                if note not in data_in_db:
                    ...
#                    model_keys[key].create(**note)

#        for key in json_data:
#            __model_object = model_keys.get(key)
#
#            if not __model_object:
#                continue
#
#            data_in_config: set = {tuple(i.values()) for i in json_data.get(key)}
#            already_exist_data: set = {tuple(model_to_dict(i).values()) for i in __model_object.select().execute()}
#
#            print(json_data.get(key))
#            print(data_in_config)
#            print(already_exist_data)
#
#            print(data_in_config.difference(already_exist_data))
#
#            break


#            data = []
#            for model_object in model_keys[key]:
#                data.append(model_to_dict(model_object))

#            print(json_data[key], data)
#            for item in json_data[key]:
#                model_keys[key].create(**item)
