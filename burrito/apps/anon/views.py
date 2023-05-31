from playhouse.shortcuts import model_to_dict

from burrito.models.liked_model import Liked
from burrito.models.tickets_model import Tickets

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
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
from burrito.utils.tickets_util import (
    hide_ticket_body,
    make_short_user_data
)


async def anon__get_ticket_list_by_filter(filters: AnonTicketListRequestSchema):
    available_filters = {
        "anonymous": Tickets.anonymous == filters.anonymous,
        "faculty": Tickets.faculty == FacultyStrToInt.convert(filters.faculty),
        "queue": Tickets.queue == QueueStrToInt.convert(filters.queue),
        "status": Tickets.status == StatusStrToInt.convert(filters.status)
    }

    final_filters = []
    for filter_item in filters.dict().items():
        if filter_item[1] is not None:
            final_filters.append(available_filters[filter_item[0]])

    response_list: AnonTicketDetailInfoSchema = []

    expression: list[Tickets] = None
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
        if not ticket.anonymous:
            creator = make_short_user_data(
                ticket.creator,
                hide_user_id=True
            )

        assignee = None
        if ticket.assignee:
            assignee = make_short_user_data(
                ticket.assignee,
                hide_user_id=True
            )

        upvotes = Liked.select().where(
            Liked.ticket_id == ticket.ticket_id
        ).count()

        response_list.append(
            AnonTicketDetailInfoSchema(
                creator=creator,
                assignee=assignee,
                ticket_id=ticket.ticket_id,
                subject=ticket.subject,
                body=hide_ticket_body(ticket.body, 500),
                faculty=FacultyResponseSchema(
                    **model_to_dict(ticket.faculty)
                ),
                status=StatusResponseSchema(
                    **model_to_dict(ticket.status)
                ),
                upvotes=upvotes,
                date=str(ticket.created)
            )
        )

    return AnonTicketListResponseSchema(
        ticket_list=response_list
    )
