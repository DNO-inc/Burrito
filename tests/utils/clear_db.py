from burrito.utils.db_utils import (
    create_tables,
    drop_tables
)

drop_tables(True)
create_tables()
