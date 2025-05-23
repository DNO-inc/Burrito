import math

from playhouse.shortcuts import model_to_dict

from burrito.models.liked_model import Liked
from burrito.models.queues_model import Queues
from burrito.models.tickets_model import Tickets
from burrito.schemas.anon_schema import (
    AnonTicketDetailInfoSchema,
    AnonTicketListRequestSchema,
    AnonTicketListResponseSchema,
)
from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.utils.query_util import (
    q_is_anonymous,
    q_is_valid_faculty,
    q_is_valid_queue,
    q_is_valid_status_list,
    q_not_hidden,
    q_protected_statuses,
    q_scope_is,
)
from burrito.utils.tickets_util import (
    get_filtered_tickets,
    hide_ticket_body,
    make_short_user_data,
    select_filters,
)


async def anon__get_ticket_list_by_filter(filters: AnonTicketListRequestSchema):
    available_filters = {
        "default": [
            q_is_anonymous(filters.anonymous),
            q_is_valid_faculty(filters.faculty),
            q_is_valid_status_list(filters.status),
            q_scope_is(filters.scope),
            q_is_valid_queue(filters.queue),
            q_not_hidden(),
            q_protected_statuses()
        ]
    }
    final_filters = select_filters("", available_filters)
    expression: list[Tickets] = get_filtered_tickets(
        final_filters,
        start_page=filters.start_page,
        tickets_count=filters.items_count
    )

    response_list: list[AnonTicketDetailInfoSchema] = []
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

        queue: Queues | None = None
        if ticket.queue:
            queue = Queues.get_or_none(Queues.queue_id == ticket.queue)

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
                queue=QueueResponseSchema(
                    queue_id=queue.queue_id,
                    faculty=queue.faculty.faculty_id,
                    name=queue.name,
                    scope=queue.scope
                ) if queue else None,
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
        ).count()/filters.items_count)
    )
