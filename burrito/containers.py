from pathlib import Path
import inspect

from burrito.utils.config_reader import get_config

from burrito.init.init_system import InitManager
from burrito.init.tasks.check_db_task import CheckDBTask
from burrito.init.tasks.preprocessor_task import PreProcessorTask


def get_current_app_name() -> str:
    return Path(inspect.getouterframes(inspect.currentframe(), 2)[1][1]).parent.name


def prepare_app():
    get_config()  # read configs

    init_manager = InitManager(
        error_attempt_delta=3
    )
    init_manager.add_task(CheckDBTask(attempt_count=100))
    init_manager.add_task(PreProcessorTask(attempt_count=100))

    init_manager.run_cycle()

    return True
