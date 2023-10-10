

class BurritoBasePlugin:
    @staticmethod
    def execute(*args, **kwargs):
        raise NotImplementedError("You can not call method of abstract class")
