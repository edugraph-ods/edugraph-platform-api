from fastapi import HTTPException, status

"""
not_found is a function that returns a 404 HTTPException.

Args:
    detail (str): The detail of the exception.

Returns:
    HTTPException: A 404 HTTPException.
"""
def not_found(detail: str = "Resource not found") -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

"""
bad_request is a function that returns a 400 HTTPException.

Args:
    detail (str): The detail of the exception.

Returns:
    HTTPException: A 400 HTTPException.
"""
def bad_request(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

"""
unauthorized is a function that returns a 401 HTTPException.

Args:
    detail (str): The detail of the exception.

Returns:
    HTTPException: A 401 HTTPException.
"""
def unauthorized(detail: str = "Unauthorized") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
