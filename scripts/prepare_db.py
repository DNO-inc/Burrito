from burrito.utils.db_utils import create_tables
from burrito.apps.scheduler.preprocessor.core import preprocessor_task


create_tables()
preprocessor_task()
