from fastapi import Depends

from fastapi_jwt_auth import AuthJWT

from burrito.utils.db_utils import get_user_by_login

from burrito.models.tickets_model import Tickets
from burrito.models.user_model import Users


async def my_reports(Authorize: AuthJWT = Depends()):
    """View all reports created by current user"""

    Authorize.jwt_required()

    user: Users | bool = get_user_by_login(Authorize.get_jwt_subject())
    if (user):
        print(Tickets.select(Tickets.issuer == user))


async def to_me(Authorize: AuthJWT = Depends()):
    """View all reports created by other users sended to current user"""
    Authorize.jwt_required()


async def followed(Authorize: AuthJWT = Depends()):
    """View all reports that current user have followed"""
    Authorize.jwt_required()


async def create_new_report(Authorize: AuthJWT = Depends()):
    """Create report"""
    Authorize.jwt_required()
