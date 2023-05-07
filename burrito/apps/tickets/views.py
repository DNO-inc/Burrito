from fastapi import Depends
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from burrito.schemas.tickets_schema import (
    CreateTicket,
    TicketIDValue,
    UpdateTicket
)
from burrito.models.tickets_model import Tickets

from .utils import (
    get_auth_core,
    is_ticket_exist,
    update_ticket_info,
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

        ticket: Tickets = Tickets.create(**ticket_creation_data.dict())

        return JSONResponse(
            status_code=200,
            content={
                "detail": "Ticket was created successfully",
                "ticket_id": ticket.ticket_id
            }
        )


class DeleteTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def delete(
        deletion_ticket_data: TicketIDValue,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        """Delete ticket"""
        Authorize.jwt_required()

        try:
            ticket: Tickets | None = is_ticket_exist(
                deletion_ticket_data.ticket_id
            )

            if not (ticket.creator.user_id == Authorize.get_jwt_subject()):
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "detail": "You have not permissions to delete this ticket"
                    }
                )

            ticket.delete_instance()

        except:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {deletion_ticket_data.ticket_id} is not exist"
                }
            )

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket was deleted successfully"}
        )


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
    async def post(
        updates: UpdateTicket,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        """Update ticket info"""
        Authorize.jwt_required()

        try:
            ticket: Tickets | None = is_ticket_exist(
                updates.ticket_id
            )

            if not (ticket.creator.user_id == Authorize.get_jwt_subject()):
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "detail": "You have not permissions to delete this ticket"
                    }
                )

            update_ticket_info(ticket, updates)

        except:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {updates.ticket_id} is not exist"
                }
            )

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket was updated successfully"}
        )


class CloseTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(Authorize: AuthJWT = Depends(get_auth_core())):
        """Close ticket"""
        Authorize.jwt_required()
