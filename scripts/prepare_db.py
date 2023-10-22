from burrito.utils.db_utils import create_tables
from burrito.utils.tasks.preprocessor import preprocessor_task
from burrito.plugins.loader import PluginLoader


PluginLoader.load()

create_tables()
preprocessor_task()
