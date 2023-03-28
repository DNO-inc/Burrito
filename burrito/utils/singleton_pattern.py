
def singleton(class_):
    """Singleton decorator"""

    class_instance = {}

    def get_class_instance(*args, **kwargs):
        if class_ not in class_instance:
            class_instance[class_] = class_(*args, **kwargs)

        return class_instance[class_]

    return get_class_instance
