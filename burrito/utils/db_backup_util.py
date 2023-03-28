"""
    Make database backup via calling backup command.

"""


import asyncio
#import subprocess

import aioschedule as schedule

from burrito.utils.logger import logger


async def do_database_backup():
    """Run backup command"""

#    subprocess.call("ls")
    logger.info("Database backup was created")


def setup_scheduler():
    """Connect tasks to scheduler"""

    schedule.every(1).seconds.do(do_database_backup)
#    schedule.every().day.at("00:00").do(do_database_backup)


async def backup_cycle(delta_time: int = 1):
    """Main scheduler cycle"""

    logger.info(f"Run backup cycle (timeout {delta_time})")
    setup_scheduler()

    loop = asyncio.get_running_loop()
    while True:
        await loop.create_task(schedule.run_pending())
        await asyncio.sleep(delta_time)
