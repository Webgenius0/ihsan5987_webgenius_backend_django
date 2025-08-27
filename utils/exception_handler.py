from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):  # check if it's a throttling exception
        custom_response_data = {
            "success": False,
            "error": "Too many requests",
            "available_in": exc.wait,  # seconds to wait before next request
            "message": f"Rate limit exceeded. Try again in {exc.wait} seconds.",
        }
        return Response(custom_response_data, status=response.status_code)

    return response
