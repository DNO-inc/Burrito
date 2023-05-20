from burrito.utils.base_view import BaseView
from burrito import __version__

from .utils import get_changelog, get_contributors


async def about__get_current_version():
    """_summary_

    Returns Burrito version
    """

    return {"version": __version__}


async def about__get_changelog_info():
    """_summary_

    Return project changelog
    """

    return {
        "changelog": get_changelog()
    }


async def about__get_info_about_team():
    """_summary_

    Return information about contributors
    """

    return {
        "team": get_contributors()
    }
