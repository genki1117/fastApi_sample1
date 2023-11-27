from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ItemStates(Enum):
    ON_SALE = 'ON_SALE',
    SOLD_OUT = 'SOLD_OUT'

class itemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, examples=["PC"])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(default=None, examples=['備品です'])

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None,min_length=2, max_length=20, examples=['PC'])
    price: Optional[int] =Field(default=None, gt=0, examples=[10000])
    description: Optional[str] = Field(default=None, examples=['備品です'])
    status: Optional[ItemStates] = Field(default=None, examples=[ItemStates.SOLD_OUT])

class ItemResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    name: str = Field(min_length=2, max_length=20, examples=['PC'])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(default=None, examples=['備品です'])
    status: ItemStates = Field(examples=[ItemStates.ON_SALE])
    created_at: datetime
    updated_at: datetime

    # ORMのmodelオブジェクトを受け取り適切なレスポンススキーマに変換する
    model_config = ConfigDict(from_attributes=True)