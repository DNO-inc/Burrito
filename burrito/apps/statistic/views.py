from fastapi import Depends
from fastapi.responses import JSONResponse

from peewee import MySQLDatabase

from playhouse.shortcuts import model_to_dict

from burrito.utils.auth import BurritoJWT, get_auth_core, AuthTokenPayload
from burrito.utils.permissions_checker import check_permission
from burrito.utils.db_cursor_object import get_database_cursor
from burrito.utils.mongo_util import get_mongo_cursor, _MONGO_DB_NAME

from burrito.models.statistic_model import (
    StatusesStatistic, FacultyScopesStatistic, ScopesStatistic,
    FacultyTicketsStatistic
)


async def statistic__periodic(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    return JSONResponse(
        content={
            "statuses": [
                model_to_dict(i) for i in StatusesStatistic.raw("SELECT * FROM tickets_by_statuses")
            ],
            "faculty_scopes": [
                model_to_dict(i) for i in FacultyScopesStatistic.raw("SELECT * FROM tickets_by_faculties_scopes")
            ],
            "scopes": [
                model_to_dict(i) for i in ScopesStatistic.raw("SELECT * FROM tickets_by_scopes")
            ]
        }
    )


async def statistic__faculties(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    return JSONResponse(
        content={
            "faculties_data": [
                model_to_dict(i) for i in FacultyTicketsStatistic.raw("SELECT * FROM faculties_by_tickets")
            ]
        }
    )


async def statistic__activity_summary(__auth_obj: BurritoJWT = Depends(get_auth_core())):
    token_payload: AuthTokenPayload = await __auth_obj.require_access_token()
    check_permission(token_payload, {"ADMIN"})

    db: MySQLDatabase = get_database_cursor()
    mongo_cursor = get_mongo_cursor()

    result = mongo_cursor[_MONGO_DB_NAME]["ticket_history"].aggregate(
        [
            {
                "$match": {
                    "field_name": "status",
                    "$or": [
                        {"new_value": "ACCEPTED"},
                        {"new_value": "CLOSE"}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$ticket_id",
                    "minValue": {"$min": "$creation_date"},
                    "maxValue": {"$max": "$creation_date"},
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "minValue": 1,
                    "maxValue": 1,
                    "delta": {
                        "$divide": [
                            {
                                "$abs": {
                                    "$subtract": [
                                        {"$dateFromString": {"dateString": "$maxValue"}},
                                        {"$dateFromString": {"dateString": "$minValue"}}
                                    ]
                                }
                            },
                            24 * 60 * 60 * 1000
                        ]
                    }
                }
            }
        ]
    )
    result = list(filter(lambda x: x["delta"], result))

    day_sum = 0
    for i in result:
        day_sum += i["delta"]

    return JSONResponse(
        content={
            "average_process_time": 0 if not result else round(day_sum / len(result), 1),
            "tickets_processed": db.execute_sql("SELECT COUNT(*) FROM tickets").fetchone()[0],
            "users_registered": db.execute_sql("SELECT COUNT(*) FROM users").fetchone()[0]
        }
    )
