from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.dao.user_dao import UserDAO  # Assuming UserDAO is appropriately implemented
from calendly.web.api.user.schemas import UserDTO, UserInputDTO  # Assuming these are located in the schemas module

router = APIRouter()


@router.get("/users/")
async def get_users(
    limit: int = 10,
    offset: int = 0,
    user_dao: UserDAO = Depends()
):
    """
    Retrieve all user objects from the database.

    :param limit: limit of user objects, defaults to 10.
    :param offset: offset of user objects, defaults to 0.
    :param user_dao: DAO for user models.
    :return: list of user objects from the database.
    """
    users = await user_dao.get_all_users(limit=limit, offset=offset)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@router.post("/users/", status_code=201)
async def create_user(
    user_input: UserInputDTO,
    user_dao: UserDAO = Depends()
):
    """
    Creates a new user in the database.

    :param user_input: DTO containing data to create a new user.
    :param user_dao: DAO for user models.
    :return: DTO of the newly created user.
    """
    user = await user_dao.create_user(name=user_input.name, email=user_input.email)
    return user
