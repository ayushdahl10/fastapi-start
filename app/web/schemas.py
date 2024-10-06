from pydantic import BaseModel

class WebConfigBase(BaseModel):
    uid:str
    key:str

class WebConfigCreate(BaseModel):
    key:str
    config:dict
    value:str
    is_active:bool

    class Config:
        from_attributes=True

class WebConfigDetail(WebConfigBase):
    config:dict
    value:str
    is_active:bool

    class Config:
        from_attributes=True
