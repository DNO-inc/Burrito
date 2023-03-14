from fastapi import Depends

from fastapi_jwt_auth import AuthJWT


async def my_reports(Authorize: AuthJWT = Depends()):
    """View all reports created by current user"""
    Authorize.jwt_required()


async def to_me(Authorize: AuthJWT = Depends()):
    """View all reports created by other users sended to current user"""
    Authorize.jwt_required()


async def followed(Authorize: AuthJWT = Depends()):
    """View all reports that current user have followed"""
    Authorize.jwt_required()


async def create_new_report(Authorize: AuthJWT = Depends()):
    """Create report"""
    Authorize.jwt_required()

