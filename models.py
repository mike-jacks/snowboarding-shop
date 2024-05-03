from enum import Enum

from sqlmodel import SQLModel, Field

from typing import Any

class Brand(str, Enum):
    NITRO = "Nitro"
    SALOMAN = "Saloman"
    BURTON = "Burton"

class Snowboard(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    length: int
    color: str
    has_bindings: bool
    brand: Brand

class CreateSnowboardRequest(SQLModel):
    length: int
    color: str
    has_bindings: bool
    brand: Brand

class PatchSnowboardRequest(SQLModel):
    length: int | None = None
    color: str | None = None
    has_bindings: bool | None = None
    brand: Brand | None = None
    

