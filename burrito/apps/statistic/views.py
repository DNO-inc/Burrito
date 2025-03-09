from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.responses import JSONResponse
from peewee import MySQLDatabase
from playhouse.shortcuts import model_to_dict

from burrito.models.statistic_model import (
    FacultyScopesStatistic,
    FacultyTicketsStatistic,
    ScopesStatistic,
    StatusesStatistic,
)
from burrito.models.user_model import Users
from burrito.utils.auth import get_current_user
from burrito.utils.db_cursor_object import get_database_cursor
from burrito.utils.mongo_util import _MONGO_DB_NAME, get_mongo_cursor


async def statistic__periodic(
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
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


async def statistic__faculties(
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):

    return JSONResponse(
        content={
            "faculties_data": [
                model_to_dict(i) for i in FacultyTicketsStatistic.raw("SELECT * FROM faculties_by_tickets")
            ]
        }
    )


async def statistic__activity_summary(
    _curr_user: Users = Depends(get_current_user(permission_list={"ADMIN"}))
):
    db: MySQLDatabase = get_database_cursor()
    mongo_cursor = get_mongo_cursor()

    curr_date = datetime.now()
    curr_month_start = curr_date.replace(day=1)
    curr_month_end = (curr_month_start + timedelta(days=32)).replace(day=1)

    result = mongo_cursor[_MONGO_DB_NAME]["ticket_history"].aggregate(
        [
            {
                "$match": {
                    "field_name": "status",
                    "creation_date": {
                        "$gte": curr_month_start,
                        "$lt": curr_month_end
                    }
                }
            },
            {
                "$group": {
                    "_id": "$ticket_id",
                    "minValue": {
                        "$min": {
                            "$cond": [
                                {
                                    "$eq": [
                                        "$new_value", "ACCEPTED"
                                    ]
                                },
                                "$creation_date", None
                            ]
                        }
                    },
                    "maxValue": {
                        "$max": {
                            "$cond": [
                                {
                                    "$eq": [
                                        "$new_value", "CLOSED"
                                    ]
                                },
                                "$creation_date", None
                            ]
                        }
                    }
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
