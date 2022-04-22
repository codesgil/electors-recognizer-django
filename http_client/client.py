import http.client
import urllib.parse
import re
import json
import socket
import traceback
import logging


class Client:
    def __init__(self, base_url='localhost', uri='', method='GET', headers={}, data=None, timeout=10):
        self.__URI = uri
        self.__refract_base_url(base_url)
        self.__METHOD = method
        self.__HEADERS = headers
        self.__TIMEOUT = timeout
        self.__make_body(data)
        self.__RESPONSE = {
            'status': '',
            'headers': {},
            'body': {}
        }

    def __refract_base_url(self, base_url):
        m = re.search("(?:(?P<PROTOCOL>http.*)://)?(?P<HOST>[^:/ ]+).?(?P<PORT>[0-9]*)(?P<URL>.*)", base_url)
        if m.group('PROTOCOL'):
            self.__CONNECTION_TYPE = m.group('PROTOCOL')
        else:
            self.__CONNECTION_TYPE = 'http'

        if m.group('HOST'):
            if m.group('PORT'):
                self.__BASE_URL = m.group('HOST') + ":" + m.group('PORT')
            else:
                self.__BASE_URL = m.group('HOST')
        else:
            self.__BASE_URL = 'localhost'
        if not self.__URI:
            self.__URI = m.group('URL')

    def __make_body(self, data):
        if self.__METHOD.upper() == 'GET':
            self.__URI = self.__URI + '?' + urllib.parse.urlencode(data)
            self.__DATA = ''
        else:
            if "Content-type" in self.__HEADERS:
                if self.__HEADERS['Content-type'] == 'application/x-www-form-urlencoded':
                    self.__DATA = urllib.parse.urlencode(data)
                else:
                    self.__DATA = json.dumps(data)
            else:
                self.__DATA = json.dumps(data)

    def __get_connection(self):
        if self.__CONNECTION_TYPE.lower() == 'https':
            conn = http.client.HTTPSConnection(self.__BASE_URL, timeout=self.__TIMEOUT)
        else:
            conn = http.client.HTTPConnection(self.__BASE_URL, timeout=self.__TIMEOUT)
        return conn

    def send_request(self):
        try:
            conn = self.__get_connection()
            conn.request(method=self.__METHOD, url=self.__URI, body=self.__DATA, headers=self.__HEADERS)
            response = conn.getresponse()
            data = response.read().decode("utf8")
            self.__RESPONSE = {
                'headers': response.getheaders(),
                'status': response.status,
                'reason': response.reason,
                'body': json.loads(str(data))
            }
            conn.close()
        except socket.gaierror as ex:
            self.__RESPONSE = {
                'body': 'Connexion Timeout',
                "status": 504
            }
            tb = traceback.format_exc()
            logging.getLogger('errors_file').error(msg=tb)
        except Exception as ex:
            self.__RESPONSE = {
                'body': ex
            }
            tb = traceback.format_exc()
            logging.getLogger('errors_file').error(msg=tb)

    def get_response(self):
        return self.__RESPONSE
