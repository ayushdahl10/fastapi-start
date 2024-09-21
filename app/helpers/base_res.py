from fastapi import HTTPException
from sqlalchemy.sql.sqltypes import Integer
from typing import Any
from fastapi.responses import JSONResponse


def success_response(content:Any,status_code:Integer=200):
    success_msg={
        "status_code":status_code,
        "data":content
    }
    return JSONResponse(content=success_msg,status_code=status_code)


def error_response(content:Any,status_code:Integer=404):
    response_msg={
        "status_code":status_code,
        "message":content,
    }
    return JSONResponse(content=response_msg,status_code=status_code)
