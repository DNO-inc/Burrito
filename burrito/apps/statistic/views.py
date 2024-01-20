from fastapi import Depends
from fastapi.responses import JSONResponse

from burrito.utils.auth import BurritoJWT, get_auth_core, AuthTokenPayload
from burrito.utils.permissions_checker import check_permission

from burrito.models.statistic_model import StatusesStatistic, FacultyScopesStatistic, ScopesStatistic


async def statistic__periodic(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    return JSONResponse(
        content={
            "by_statuses": list(StatusesStatistic.raw("SELECT * FROM tickets_by_statuses")),
            "by_faculty_scopes": list(
                FacultyScopesStatistic.raw("SELECT * FROM tickets_by_faculties_scopes")
            ),
            "by_scopes": list(ScopesStatistic.raw("SELECT * FROM tickets_by_scopes"))
        }
    )


async def statistic__faculties(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    return "Hello)"


async def statistic__activity_summary(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    return "Hello)"
