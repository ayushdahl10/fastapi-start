from fastapi import HTTPException
import re

def validate_password(func):
    def inner(self,value):
        print(value)
        if len(value) < 8:
            raise HTTPException("Password must be at least 8 characters long")
        if not re.search(r'[a-z]', value):
            raise HTTPException("Password must contain at least one lowercase letter")
        if not re.search(r'[A-Z]', value):
            raise HTTPException("Password must contain at least one uppercase letter")
        if not re.search(r'\d', value):
            raise HTTPException("Password must contain at least one digit")
        if not re.search(r'[@$!%*#?&]', value):
            raise HTTPException("Password must contain at least one special character")
        func(self,value)
    return inner
