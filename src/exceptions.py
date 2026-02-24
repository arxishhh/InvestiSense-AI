from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI,status

class InvestiSenseException(Exception):
    """
    This is the base class for all InvestiSense errors
    """
    pass

class UserNotFound(InvestiSenseException):
    """
    User with the provided credentials does not exist
    """
    pass

class InvalidToken(InvestiSenseException):
    """
    User has provided an invalid or expired token
    """
    pass

class RevokedToken(InvestiSenseException):
    """
    User has provided an invalid or expired token
    """
    pass 

class AccessTokenRequired(InvestiSenseException):
    """
    User has provided an invalid or expired token
    """
    pass

class RefreshTokenRequired(InvestiSenseException):
    """
    User has provided an invalid or expired token
    """
    pass

class UserAlreadyExists(InvestiSenseException):
    """ 
    User has provided an invalid or expired token
    """
    pass

class InvalidCredentials(InvestiSenseException):
    """
    User has provided an invalid or expired token
    """
    pass

class GraphException(InvestiSenseException):
    """
    Exception raised for errors in the graph operations
    """
    pass


def create_exception_handler(status_code : int,initial_detail : Any) -> Callable[[Request,Exception], JSONResponse]:

    async def exception_handler(request : Request, exc : Exception):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    
    return exception_handler

def register_all_errors(app : FastAPI):
    
    app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code = status.HTTP_404_NOT_FOUND,
        inital_detail = {
            "message": "User with email already exists",
            "error_code": "user_exists"
        }
    ))

    app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code = status.HTTP_403_FORBIDDEN,
        inital_detail = {
            "message": "User Not Found",
            "error_code": "user_not_found"
        }
    ))

    app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code = status.HTTP_403_FORBIDDEN,
        inital_detail = {
            "message": "Invalid Credentials",
            "error_code": "invalid_credentials"
        }
    ))

    app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code = status.HTTP_403_FORBIDDEN,
        inital_detail = {
            "message": "Token in invalid",
            "error_code": "invalid_token"
        }
    ))

    app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code = status.HTTP_403_FORBIDDEN,
        inital_detail = {
            "message": "Token is invalid or already revoked",
            "error_code": "revoked_token"
        }
    ))

    app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code = status.HTTP_403_FORBIDDEN,
        inital_detail = {
            "message": "Please provide a valid access token",
            "error_code": "access_token_required"
        }
    ))

    app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code = status.HTTP_403_FORBIDDEN,
        inital_detail = {
            "message": "Please provide a valid refresh token",
            "error_code": "refresh_token_required"
        }
    ))
    
    app.add_exception_handler(
    GraphException,
    create_exception_handler(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        inital_detail = {
            "message": "An error occurred while processing the graph operation",
            "error_code": "graph_exception"
        }
    ))

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "message" : "Oops! Something went wrong on the server.",
            "error_code": "server_error"
        })
