import math

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

from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_hidden,
    q_protected_statuses
)
from burrito.utils.tickets_util import (
    hide_ticket_body,
    make_short_user_data,
    get_filtered_tickets,
    select_filters
)


async def anon__get_ticket_list_by_filter(filters: AnonTicketListRequestSchema):
    available_filters = {
        "anonymous": q_is_anonymous(filters.anonymous),
        "faculty": q_is_valid_faculty(filters.faculty),
        "queue": q_is_valid_queue(filters.queue, filters.faculty),
        "status": q_is_valid_status_list(filters.status)
    }
    final_filters = select_filters(available_filters, filters) + [
        q_hidden(),
        q_protected_statuses()
    ]

    response_list: list[AnonTicketDetailInfoSchema] = []

    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=filters.start_page,
        tickets_count=filters.tickets_count
    )

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
        ticket_list=response_list,
        total_pages=math.ceil(Tickets.select().where(
            *final_filters
        ).count()/filters.tickets_count)
    )
