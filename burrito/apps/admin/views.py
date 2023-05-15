from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from playhouse.shortcuts import model_to_dict

from burrito.models.tickets_model import Tickets

from burrito.schemas.admin_schema import (
    AdminTicketIdSchema,
    AdminUpdateTicketSchema,
    AdminGetTicketListSchema,
    AdminTicketDetailInfo,
    AdminTicketListResponse
)

from burrito.utils.tickets_util import hide_ticket_body
from burrito.utils.auth import get_auth_core
from burrito.utils.converter import (
    StatusStrToInt,
    FacultyStrToInt,
    QueueStrToInt
)

from .utils import (
    BaseView, status,
    check_permission,
    is_ticket_exist
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

        faculty_id = FacultyStrToInt.convert(admin_updates.faculty)
        if faculty_id:  # faculty_id must be > 1
            ticket.faculty_id = faculty_id

        queue_id = QueueStrToInt.convert(admin_updates.queue)
        if queue_id:    # queue_id must be > 1
            ticket.queue_id = queue_id

        status_id = StatusStrToInt.convert(admin_updates.status)
        if status_id:    # status_id must be > 1
            ticket.status_id = status_id

        if any((faculty_id, queue_id, status_id)):
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
            "hidden": Tickets.hidden == filters.hidden,
            "anonymous": Tickets.anonymous == filters.anonymous,
            "faculty": Tickets.faculty_id == FacultyStrToInt.convert(filters.faculty),
            "queue": Tickets.queue_id == QueueStrToInt.convert(filters.queue),
            "status": Tickets.status_id == StatusStrToInt.convert(filters.status)
        }

        final_filters = []

        for filter_item in filters.dict().items():
            if filter_item[1] is not None:
                final_filters.append(available_filters[filter_item[0]])

        response_list: AdminTicketDetailInfo = []

        expression = None
        if final_filters:
            expression = Tickets.select().where(*final_filters)
        else:
            # TODO: make pagination
            expression = Tickets.select()

        for ticket in expression:
            creator = None
            assignee = None
            if not ticket.anonymous:
                creator = model_to_dict(ticket.creator)
                creator["faculty"] = ticket.creator.faculty_id.name

                assignee = ticket.assignee
                assignee_modified = dict()
                if assignee:
                    assignee_modified = model_to_dict(assignee)
                    assignee_modified["faculty"] = ticket.assignee.faculty_id.name

            response_list.append(
                AdminTicketDetailInfo(
                    creator=creator,
                    assignee=assignee_modified if assignee else None,
                    ticket_id=ticket.ticket_id,
                    subject=ticket.subject,
                    body=hide_ticket_body(ticket.body),
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
    async def post(
        ticket_id_info: AdminTicketIdSchema,
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

        creator = None
        if not ticket.anonymous:
            creator = model_to_dict(ticket.creator)
            creator["faculty"] = ticket.creator.faculty_id.name
            creator["group"] = ticket.creator.group_id.name

        assignee = ticket.assignee
        if assignee:
            assignee = model_to_dict(assignee)
            assignee["faculty"] = ticket.assignee.faculty_id.name
            assignee["group"] = ticket.assignee.group_id.name

        return AdminTicketDetailInfo(
            creator=creator,
            assignee=assignee,
            ticket_id=ticket.ticket_id,
            subject=ticket.subject,
            body=ticket.body,
            queue=ticket.queue_id.name if ticket.queue_id else None,
            faculty=ticket.faculty_id.name,
            status=ticket.status_id.name
        )


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
