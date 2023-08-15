import inspect
from pprint import pprint


def check_error(foo, foo_args: dict, response = None):
    try:
        foo(**foo_args)
    except Exception as e:
        pprint(
            {
                "name_of_test": inspect.stack()[1][3],
                "response": response.json() if response is not None and not isinstance(response, dict) else response,
                "exception": e,
            }
        )
        print()
