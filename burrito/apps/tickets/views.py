from fastapi import Depends

from fastapi_jwt_auth import AuthJWT

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users

from .utils import get_auth_core, get_user_by_login, BaseView, check_permission


class CreateTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(Authorize: AuthJWT = Depends(get_auth_core())):
        """Create ticket"""
        Authorize.jwt_required()


class DeleteTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def delete(Authorize: AuthJWT = Depends(get_auth_core())):
        """Delete ticket"""
        Authorize.jwt_required()


class FollowTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(Authorize: AuthJWT = Depends(get_auth_core())):
        """Follow ticket"""
        Authorize.jwt_required()


class TicketListView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(Authorize: AuthJWT = Depends(get_auth_core())):
        """Show tickets"""
        Authorize.jwt_required()


class TicketDetailInfoView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(Authorize: AuthJWT = Depends(get_auth_core())):
        """Show detail ticket info"""
        Authorize.jwt_required()


class UpdateTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(Authorize: AuthJWT = Depends(get_auth_core())):
        """Update ticket info"""
        Authorize.jwt_required()


class CloseTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(Authorize: AuthJWT = Depends(get_auth_core())):
        """Close ticket"""
        Authorize.jwt_required()
