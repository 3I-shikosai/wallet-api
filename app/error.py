from pydantic import BaseModel


class ErrorResponseFormat(BaseModel):
    message: str
    error_code: int


class ErrorResponse:
    PASSWORD_INCORRECT = ErrorResponseFormat(
        message="PASSWORD_INCORRECT", error_code=1
    ).model_dump()

    USER_NOT_FOUND = ErrorResponseFormat(
        message="USER_NOT_FOUND", error_code=2
    ).model_dump()

    USER_CREATION_FAILED = ErrorResponseFormat(
        message="USER_CREATION_FAILED", error_code=3
    ).model_dump()

    USER_DELETION_FAILED = ErrorResponseFormat(
        message="USER_DELETION_FAILED", error_code=4
    ).model_dump()
    USER_ALREADY_LOGGED_IN = ErrorResponseFormat(
        message="USER_ALREADY_LOGGED_IN", error_code=5
    ).model_dump()
