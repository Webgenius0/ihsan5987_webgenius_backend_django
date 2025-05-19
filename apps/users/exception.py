# apps/core/exception.py
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationFailed) and response is not None:
        if isinstance(exc.detail, dict) and 'error' in exc.detail:
            response.data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "success": False,
                "error": exc.detail.get('error')
            }
    return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)

