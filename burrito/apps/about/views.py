from burrito.utils.base_view import BaseView
from burrito import __version__

from .utils import get_changelog, get_contributors


class VersionView(BaseView):
    _permissions: list[str] = []

    @staticmethod
    async def get():
        return {"version": __version__}


class UpdatesView(BaseView):
    _permissions: list[str] = []

    @staticmethod
    async def get():
        return {
            "changelog": get_changelog()
        }


class TeamView(BaseView):
    _permissions: list[str] = []

    @staticmethod
    async def get():
        return {
            "team": get_contributors()
        }
