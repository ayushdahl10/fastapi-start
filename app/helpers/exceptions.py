from fastapi import HTTPException
from typing_extensions import Annotated, Doc
from typing import Dict, Any, Optional


class BaseException(HTTPException):
    def __init__(
        self,
        status_code: Annotated[
            int,
            Doc(
                """
        HTTP status code to send to the client.
        """
            ),
        ],
        detail: Annotated[
            Any,
            Doc(
                """
            Any data to be sent to the client in the `detail` key of the JSON
            response.
            """
            ),
        ] = None,
        headers: Annotated[
            Optional[Dict[str, str]],
            Doc(
                """
                Any headers to send to the client in the response.
                """
            ),
        ] = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
