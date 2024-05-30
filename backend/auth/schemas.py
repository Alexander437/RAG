from pydantic import BaseModel, Field


class UserDBConfig(BaseModel):
    db_name: str = Field(min_length=1, frozen=True)
    db_user: str = Field(min_length=1, frozen=True)
    db_pass: str = Field(min_length=1, frozen=True)
    db_host: str = Field(min_length=1, frozen=True)
    db_port: int = Field(gt=1023, frozen=True)

    @property
    def get_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
