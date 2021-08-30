from rest_framework import status
from rest_framework.response import Response


def response_http_400(message):
    return Response(
        {
            "message": message,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )
