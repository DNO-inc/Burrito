"""
    Make database backup via calling backup command.

"""


import asyncio
# import subprocess

import aioschedule as schedule

from burrito.utils.logger import get_logger
from burrito.utils.task_manager import get_async_manager


async def do_database_backup() -> None:
    """_summary_

        Run backup command
    """

#    subprocess.call("ls")
    get_logger().info("Database backup was created")


def setup_scheduler():
    """_summary_

        Connect tasks to scheduler
    """

    schedule.every(1).seconds.do(do_database_backup)
#    schedule.every().day.at("00:00").do(do_database_backup)


async def backup_cycle(delta_time: int = 1):
    """_summary_

    Main scheduler cycle

    Args:
        delta_time (int, optional): cycle timeout. Defaults to 1.
    """

    get_logger().info(f"Run backup cycle (timeout {delta_time})")
    setup_scheduler()

    while True:
        await get_async_manager().loop.create_task(schedule.run_pending())
        await asyncio.sleep(delta_time)
