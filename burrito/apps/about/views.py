from burrito import __version__

from .utils import get_changelog, get_contributors


async def about__get_current_version():
    """
    Returns Burrito version
    """

    return {"version": __version__}


async def about__get_changelog_info():
    """
    Return project changelog
    """

    return {
        "changelog": get_changelog()
    }


async def about__get_info_about_team():
    """
    Return information about contributors
    """

    return {
        "team": get_contributors()
    }
