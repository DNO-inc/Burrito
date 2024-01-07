from fastapi import HTTPException

from burrito.utils.permissions_checker import check_permission

from burrito.models.tickets_model import Tickets
from burrito.models.queues_model import Queues
from burrito.models.liked_model import Liked
from burrito.models.user_model import Users
from burrito.models.roles_model import Roles

from burrito.schemas.faculty_schema import FacultyResponseSchema
from burrito.schemas.status_schema import StatusResponseSchema
from burrito.schemas.queue_schema import QueueResponseSchema
from burrito.schemas.admin_schema import AdminTicketDetailInfo
from burrito.schemas.profile_schema import AdminRequestUpdateProfileSchema

from burrito.utils.auth import AuthTokenPayload
from burrito.utils.converter import (
    FacultyConverter,
    GroupConverter
)
from burrito.utils.users_util import get_user_by_id, get_user_by_login
from burrito.utils.validators import (
    is_valid_firstname,
    is_valid_lastname,
    is_valid_login,
    is_valid_phone
)
from burrito.utils.tickets_util import (
    is_ticket_exist,
    is_ticket_followed,
    is_ticket_bookmarked,
    is_ticket_liked,
    hide_ticket_body
)


__all__ = [
    "is_ticket_exist",
    "check_permission"
]


def make_ticket_detail_info(
        ticket: Tickets,
        token_payload: AuthTokenPayload,
        creator: Users | None,
        assignee: Users | None,
        *,
        crop_body: bool = True
) -> AdminTicketDetailInfo:

    queue: Queues | None = None
    if ticket.queue:
        queue = Queues.get_or_none(Queues.queue_id == ticket.queue)

    return AdminTicketDetailInfo(
        creator=creator,
        assignee=assignee,
        ticket_id=ticket.ticket_id,
        subject=ticket.subject,
        body=hide_ticket_body(ticket.body, 500) if crop_body else ticket.body,
        hidden=ticket.hidden,
        anonymous=ticket.anonymous,
        faculty=FacultyResponseSchema(
            faculty_id=ticket.faculty.faculty_id,
            name=ticket.faculty.name
        ),
        queue=QueueResponseSchema(
            queue_id=queue.queue_id,
            faculty=queue.faculty.faculty_id,
            name=queue.name,
            scope=queue.scope
        ) if queue else None,
        status=StatusResponseSchema(
            status_id=ticket.status.status_id,
            name=ticket.status.name,
        ),
        upvotes=Liked.select().where(
            Liked.ticket_id == ticket.ticket_id
        ).count(),
        is_liked=is_ticket_liked(token_payload.user_id, ticket.ticket_id),
        is_followed=is_ticket_followed(token_payload.user_id, ticket.ticket_id),
        is_bookmarked=is_ticket_bookmarked(token_payload.user_id, ticket.ticket_id),
        date=str(ticket.created)
    )


async def update_profile_as_admin(
    user_id: int,
    profile_updated_data: AdminRequestUpdateProfileSchema | None = AdminRequestUpdateProfileSchema(),
    allow_extra_fields: bool = False
) -> None:
    current_user: Users | None = get_user_by_id(user_id)

    if is_valid_firstname(profile_updated_data.firstname):
        current_user.firstname = profile_updated_data.firstname

    if is_valid_lastname(profile_updated_data.lastname):
        current_user.lastname = profile_updated_data.lastname

    if is_valid_login(profile_updated_data.login):
        # user can provide their own login, so we should not raise en error
        if current_user.login != profile_updated_data.login and get_user_by_login(profile_updated_data.login):
            raise HTTPException(
                status_code=403,
                detail="User with the same login exists"
            )

        current_user.login = profile_updated_data.login

    if is_valid_phone(profile_updated_data.phone):
        current_user.phone = profile_updated_data.phone

    # check faculty
    if profile_updated_data.faculty:
        faculty_id = FacultyConverter.convert(profile_updated_data.faculty)
        if faculty_id:
            current_user.faculty = faculty_id

    # check group
    if profile_updated_data.group:
        group_id = GroupConverter.convert(profile_updated_data.group)
        if group_id:
            current_user.group = group_id

    if (
        allow_extra_fields
        and profile_updated_data.role_id
        and Roles.get_or_none(Roles.role_id == profile_updated_data.role_id)
    ):
        current_user.role = profile_updated_data.role_id

    current_user.save()
