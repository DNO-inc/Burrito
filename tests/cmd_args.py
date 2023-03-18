import argparse


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8080

parser = argparse.ArgumentParser()
parser.add_argument(
    "-H",
    "--host",
    type=str,
    default=DEFAULT_HOST,
    help="IP of an Rest API server"
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help="port that listened by Burrito"
)
