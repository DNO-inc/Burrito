from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from playhouse.shortcuts import model_to_dict

from burrito.schemas.admin_schema import (
    AdminTicketIdSchema,
    AdminUpdateTicketSchema,
    AdminGetTicketListSchema,
    AdminTicketDetailInfo,
    AdminTicketListResponse
)
from burrito.utils.auth import get_auth_core

from .utils import (
    BaseView, status, check_permission, is_ticket_exist,
    Tickets
)


class AdminUpdateTicketsView(BaseView):
    _permissions: list[str] = ["ADMIN"]

    @staticmethod
    @check_permission
    async def post(
        admin_updates: AdminUpdateTicketSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
        Authorize.jwt_required()

        ticket: Tickets | None = is_ticket_exist(
            admin_updates.ticket_id
        )

        if not ticket:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": f"ticket_id {admin_updates.ticket_id} is not exist"
                }
            )

        if admin_updates.faculty_id:  # faculty_id must be > 1
            ticket.faculty_id = admin_updates.faculty_id

        if admin_updates.queue_id:    # queue_id must be > 1
            ticket.queue_id = admin_updates.queue_id

        if admin_updates.status_id:    # status_id must be > 1
            ticket.status_id = admin_updates.status_id

        if any(
            [
                admin_updates.faculty_id,
                admin_updates.queue_id,
                admin_updates.status_id
            ]
        ):
            ticket.save()

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket data was updated successfully"}
        )


class AdminGetTicketListView(BaseView):
    _permissions: list[str] = ["ADMIN"]

    @staticmethod
    @check_permission
    async def post(
        filters: AdminGetTicketListSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
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

        response_list: AdminTicketDetailInfo = []

        for ticket in Tickets.select().where(*final_filters):
            assignee = ticket.assignee
            response_list.append(
                AdminTicketDetailInfo(
                    creator=model_to_dict(ticket.creator),
                    assignee=model_to_dict(assignee) if assignee else None,
                    ticket_id=ticket.ticket_id,
                    subject=ticket.subject,
                    body=ticket.body,
                    faculty=ticket.faculty_id.name,
                    status=ticket.status_id.name
                )
            )

        return AdminTicketListResponse(
            ticket_list=response_list
        )


class AdminTicketDetailInfoView(BaseView):
    _permissions: list[str] = ["ADMIN"]

    @staticmethod
    @check_permission
    async def post():
        ...


class AdminDeleteTicketView(BaseView):
    _permissions: list[str] = ["ADMIN"]

    @staticmethod
    @check_permission
    async def post(
        deletion_ticket_data: AdminTicketIdSchema,
        Authorize: AuthJWT = Depends(get_auth_core())
    ):
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

        ticket.delete_instance()

        return JSONResponse(
            status_code=200,
            content={"detail": "Ticket was deleted successfully"}
        )


class AdminChangePermissionsView(BaseView):
    _permissions: list[str] = ["ADMIN"]

    @staticmethod
    @check_permission
    async def post():
        return {"1": 1}
