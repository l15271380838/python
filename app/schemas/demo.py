from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateItemRequest(BaseModel):
    name:str=Field(min_length=1,max_length=100,description="商品name")
    price:float=Field(gt=1,description="价格，要大于0")
    description:Optional[str]=Field(default=None,max_length=500,description="描述")
    is_active:bool=Field(default=True,description="是否上架")

class ItemResponse(BaseModel):
    id:int
    name:str
    price:float
    description:Optional[str]=None
    is_active:bool
    create_at:datetime
    model_config = {"from_attributes": True}