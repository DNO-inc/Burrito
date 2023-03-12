import logging


# Creating custom Formatter
class BurritoFormatter(logging.Formatter):
    # Defining colors
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = "\u001b[32m"
    red = "\x1b[31;20m"
    magenta = "\u001b[35m"
    reset = "\x1b[0m"
    format = "[ %(asctime)s ] | %(name)s | %(levelname)s:  %(message)s (%(filename)s:%(lineno)d)"

    # Defining formats
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: magenta + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Creating Custom logger
logger = logging.getLogger("burrito")
logger.setLevel(logging.DEBUG)

# Creating console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(BurritoFormatter())

# Defining handler
logger.addHandler(ch)
