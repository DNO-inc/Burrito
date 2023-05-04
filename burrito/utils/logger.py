import logging

from burrito.utils.singleton_pattern import singleton


# Creating custom Formatter
class BurritoFormatter(logging.Formatter):
    # Defining colors
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = "\u001b[32m"
    red = "\x1b[31;20m"
    magenta = "\u001b[35m"
    reset = "\x1b[0m"
    _format = "[ %(asctime)s ] | %(name)s | %(levelname)s: %(message)s (%(filename)s:%(lineno)d)"

    # Defining formats
    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: green + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: magenta + _format + reset
    }

    def format(self, record):
        """_summary_

        Setup logger format

        Args:
            record (_type_): _description_

        Returns:
            str: logger format
        """

        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


@singleton
class BurritoLogger(logging.Logger):
    def __init__(self, name: str, level: int) -> None:
        """_summary_

        Args:
            name (str): logger name
            level (int): logging level
        """

        super().__init__(name, level)

        # Creating console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(BurritoFormatter())

        self.addHandler(ch)


def get_logger(level: int = logging.DEBUG) -> BurritoLogger:
    """_summary_

    Args:
        level (int, optional): logging level. Defaults to logging.DEBUG.

    Returns:
        BurritoLogger: logger object
    """

    return BurritoLogger("burrito", level)
