from pathlib import Path
import sys
import os

sys.path.append(
    Path(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    ).__str__()
)

from burrito.utils.db_utils import (
    create_tables,
    drop_tables
)

drop_tables(True)
create_tables()
