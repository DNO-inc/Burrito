
from typing import Any


def singleton(class_) -> Any:
    """_summary_

    Singleton decorator

    Args:
        class_ (_type_): class_

    Returns:
        _type_: return single class instance
    """

    class_instance = {}

    def get_class_instance(*args, **kwargs):
        if class_ not in class_instance:
            class_instance[class_] = class_(*args, **kwargs)

        return class_instance[class_]

    return get_class_instance
