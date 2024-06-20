import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, Field, EmailStr


class UserRead(schemas.BaseUser):
    id: uuid.UUID
    role_id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    username: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserDBConfig(BaseModel):
    db_name: str = Field(min_length=1, frozen=True)
    db_user: str = Field(min_length=1, frozen=True)
    db_pass: str = Field(min_length=1, frozen=True)
    db_host: str = Field(min_length=1, frozen=True)
    db_port: str = Field(min_length=1, frozen=True)

    @property
    def get_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


class SMTPConfig(BaseModel):
    host: str = Field(min_length=1, frozen=True)
    port: int = Field(frozen=True)
    user: str = Field(min_length=1, frozen=True)
    password: str = Field(min_length=1, frozen=True)
