import logging
import socket


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        logging.basicConfig()
        logging.getLogger('access_file').info(msg=str(self.build_logging_data(request=request)))

        return response

    def build_logging_data(self, request):
        data = {
            'request': self.build_request_logger(request=request)
        }
        return data

    def build_request_logger(self, request):
        return {
            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'user_agent': request.headers['User-Agent'],
            'request_method': request.method,
            'request_path': request.get_full_path()
        }
