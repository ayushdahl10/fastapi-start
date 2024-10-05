from pydantic import BaseModel

class WebConfigCreate(BaseModel):
    uid:str
    key:str
    config:dict
    value:str
    is_active:bool

    class Config:
        from_attributes=True
