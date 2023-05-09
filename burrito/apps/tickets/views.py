from fastapi import Depends
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT

from playhouse.shortcuts import model_to_dict

from burrito.schemas.tickets_schema import (
    CreateTicket,
    TicketIDValue,
    UpdateTicket,
    TicketDetailInfo,
    TicketList,
    TicketListResponse
)
from burrito.models.tickets_model import Tickets
from burrito.models.statuses_model import Statuses
from burrito.models.bookmarks_model import Bookmarks

from burrito.utils.logger import get_logger

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

        ticket: Tickets | None = is_ticket_exist(
            deletion_ticket_data.ticket_id
        )

        if not ticket:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {deletion_ticket_data.ticket_id} is not exist"
                }
            )

        if not (ticket.creator.user_id == Authorize.get_jwt_subject()):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": "You have not permissions to delete this ticket"
                }
            )

        ticket.delete_instance()

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket was deleted successfully"}
        )


class BookmarkTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(
        bookmark_ticket_data: TicketIDValue,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        """Follow ticket"""
        Authorize.jwt_required()

        ticket: Tickets | None = is_ticket_exist(
            bookmark_ticket_data.ticket_id
        )

        if not ticket:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {bookmark_ticket_data.ticket_id} is not exist"
                }
            )

        try:
            Bookmarks.create(
                user_id=Authorize.get_jwt_subject(),
                ticket_id=ticket.ticket_id
            )
        except:
            ...

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket was bookmarked successfully"}
        )


class TicketListView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(
        filters: TicketList,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        """Show tickets"""
        Authorize.jwt_required()

        available_filters = {
            "creator": Tickets.creator == filters.creator,
            "hidden": Tickets.hidden == filters.hidden,
            "anonymous": Tickets.anonymous == filters.anonymous,
            "faculty_id": Tickets.faculty_id == filters.faculty_id,
            "queue_id": Tickets.queue_id == filters.queue_id,
            "status_id": Tickets.status_id == filters.status_id
        }

        final_filters = []

        for filter_item in filters.dict().items():
            if filter_item[1] is not None:
                final_filters.append(available_filters[filter_item[0]])

        response_list: TicketDetailInfo = []

        for ticket in Tickets.select().where(*final_filters):
            assignee = ticket.assignee
            response_list.append(
                TicketDetailInfo(
                    creator=model_to_dict(ticket.creator),
                    assignee=model_to_dict(assignee) if assignee else None,
                    ticket_id=ticket.ticket_id,
                    subject=ticket.subject,
                    body=ticket.body,
                    faculty=ticket.faculty_id.name,
                    status=ticket.status_id.name
                )
            )

        return TicketListResponse(
            ticket_list=response_list
        )


class TicketDetailInfoView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(
        ticket_id_info: TicketIDValue,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        """Show detail ticket info"""
        Authorize.jwt_required()

        ticket: Tickets | None = is_ticket_exist(
            ticket_id_info.ticket_id
        )

        if not ticket:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {ticket_id_info.ticket_id} is not exist"
                }
            )

        assignee = ticket.assignee
        return TicketDetailInfo(
            creator=model_to_dict(ticket.creator),
            assignee=model_to_dict(assignee) if assignee else None,
            ticket_id=ticket.ticket_id,
            subject=ticket.subject,
            body=ticket.body,
            faculty=ticket.faculty_id.name,
            status=ticket.status_id.name
        )


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

        ticket: Tickets | None = is_ticket_exist(
            updates.ticket_id
        )

        if not ticket:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {updates.ticket_id} is not exist"
                }
            )

        if not (ticket.creator.user_id == Authorize.get_jwt_subject()):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": "You have not permissions to update this ticket"
                }
            )

        update_ticket_info(ticket, updates)

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket was updated successfully"}
        )


class CloseTicketView(BaseView):
    _permissions: list[str] = ["READ"]

    @staticmethod
    @check_permission
    async def post(
        data_to_close_ticket: TicketIDValue,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        """Close ticket"""
        Authorize.jwt_required()

        ticket: Tickets | None = is_ticket_exist(
            data_to_close_ticket.ticket_id
        )

        if not ticket:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {data_to_close_ticket.ticket_id} is not exist"
                }
            )

        if not (ticket.creator.user_id == Authorize.get_jwt_subject()):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": "You have not permissions to close this ticket"
                }
            )

        status_name = "CLOSE"
        status_object = Statuses.get_or_none(Statuses.name == status_name)

        if not status_object:
            get_logger().critical(f"Status {status_name} is not exist in database")

            return JSONResponse(
                status_code=500,
                content={"detail": "Ticket is not closed. Try latter."}
            )

        ticket.status_id = status_object
        ticket.save()

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket was closed successfully"}
        )
