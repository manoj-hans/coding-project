from pydantic import BaseModel


class UserDTO(BaseModel):
    """
    DTO for User models.

    It is returned when accessing user models from the API.
    """
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class UserInputDTO(BaseModel):
    """DTO for creating a new user."""
    name: str
    email: str
