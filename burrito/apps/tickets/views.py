from fastapi import Depends
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from burrito.schemas.tickets_schema import CreateTicket
from burrito.models.tickets_model import Tickets

from .utils import (
    get_auth_core,
    get_user_by_id,
    BaseView, status,
    check_permission
)


class CreateTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(
        ticket_creation_data: CreateTicket,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        """Create ticket"""
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        if user_id != ticket_creation_data.creator_id:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "User ID is not the same"}
            )

        Tickets.create(**ticket_creation_data.dict())


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
