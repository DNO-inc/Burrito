from playhouse.shortcuts import model_to_dict

from burrito.models.tickets_model import Tickets

from burrito.schemas.anon_schema import (
    AnonTicketListRequestSchema,
    AnonTicketDetailInfoSchema,
    AnonTicketListResponseSchema
)

from burrito.utils.converter import (
    FacultyStrToInt,
    QueueStrToInt,
    StatusStrToInt
)
from burrito.utils.tickets_util import hide_ticket_body

from .utils import BaseView


class AnonTicketListView(BaseView):
    _permissions: list[str] = []

    @staticmethod
    async def post(filters: AnonTicketListRequestSchema):
        available_filters = {
            "anonymous": Tickets.anonymous == filters.anonymous,
            "faculty": Tickets.faculty_id == FacultyStrToInt.convert(filters.faculty),
            "queue": Tickets.queue_id == QueueStrToInt.convert(filters.queue),
            "status": Tickets.status == StatusStrToInt.convert(filters.status)
        }

        final_filters = []
        for filter_item in filters.dict().items():
            if filter_item[1] is not None:
                final_filters.append(available_filters[filter_item[0]])

        response_list: AnonTicketDetailInfoSchema = []

        expression = None
        if final_filters:
            expression = Tickets.select().where(
                Tickets.hidden == 0,
                *final_filters
            )
        else:
            # TODO: make pagination
            expression = Tickets.select().where(Tickets.hidden == 0)

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
                AnonTicketDetailInfoSchema(
                    creator=creator,
                    assignee=assignee_modified if assignee else None,
                    ticket_id=ticket.ticket_id,
                    subject=ticket.subject,
                    body=hide_ticket_body(ticket.body),
                    faculty=ticket.faculty_id.name,
                    status=ticket.status.name
                )
            )

        return AnonTicketListResponseSchema(
            ticket_list=response_list
        )
