# apps/core/exception.p
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed) and response is not None:
        if isinstance(exc.detail, dict) and 'error' in exc.detail:
            response.data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "success": False,
                "error": exc.detail.get('error')
            }
        return response

    # Handle other unexpected exceptions if DRF returns None
    if response is None:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "success": False,
            "error": str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response