import logging
import re
import threading
import traceback

from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from http_client import client


def fetch_all_sql(query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    return __dict_fetch_all(cursor)


def __dict_fetch_all(cursor):
    # Returns all rows from a cursor as a dict
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def core_exception_handler(exc, context):
    # If an exception is thrown that we don't explicitly handle here, we want
    # to delegate to the default exception handler offered by DRF. If we do
    # handle this exception type, we will still want access to the response
    # generated by DRF, so we get that response up front.
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error
    }
    # This is how we identify the type of the current exception. We will use
    # this in a moment to see whether we should handle this exception or let
    # Django REST Framework do its thing.
    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        # If this exception is one that we can handle, handle it. Otherwise,
        # return the response generated earlier by the default exception
        # handler.
        return handlers[exception_class](exc, context, response)

    response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    if exception_class == 'DoesNotExist':
        response_status = status.HTTP_404_NOT_FOUND
    if exception_class == 'TokenError':
        response_status = status.HTTP_401_UNAUTHORIZED
    if response is None:
        message = str(exc)
        tb = traceback.format_exc()
        logging.getLogger('errors_file').error(msg=tb)
        message = message.strip().translate(str.maketrans('', '', '\n\t\r')).replace('"', '').replace('^', '').strip()
        return Response({'detail': message}, status=response_status)
    return response


def _handle_generic_error(exc, context, response):
    # This is the most straightforward exception handler we can create.
    # We take the response generated by DRF and wrap it in the `errors` key.
    response.data = {
        'errors': response.data
    }

    return response


def format_form_errors_response(errors):
    return {
        "errors": {
            "fields": errors
        }
    }


class HttpClientThread(threading.Thread):
    def __init__(self, base_url="localhost", uri="", method="GET", headers={}, data=None, timeout=10):
        self.base_url = base_url
        self.uri = uri
        self.method = method
        self.headers = headers
        self.data = data
        self.timeout = timeout
        threading.Thread.__init__(self)

    def run(self):
        http_request = client.Client(base_url=self.base_url, uri=self.uri, method=self.method,
                                     headers=self.headers, data=self.data, timeout=self.timeout)
        http_request.send_request()
        logging.getLogger(name="http_client_file").info(http_request.get_response())


def send_request(base_url="localhost", uri="", method="GET", headers={}, data=None, timeout=10):
    HttpClientThread(base_url, uri, method, headers, data, timeout).start()


def send_sms(phone, content, sender):
    from api.settings import SMS_API
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'x-api-key': SMS_API['BULK']['API_KEY'],
        'secret': SMS_API['BULK']['PASSWORD']
    }
    data = {
        'sender': sender,
        'phone': format_phone(phone),
        'message': content,
        'flag': 'short_sms'
    }
    send_request(base_url=SMS_API['BULK']['BASE_URL'], uri=SMS_API['BULK']['URI'],
                 method=SMS_API['BULK']['METHOD'], data=data,
                 headers=headers)


def format_phone(phone):
    result = re.match('^237', phone)
    if not result:
        phone = '237' + str(phone)
    return phone
