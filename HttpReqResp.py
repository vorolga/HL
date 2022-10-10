import mimetypes
import os
from datetime import datetime
from urllib.parse import urlparse

CRLF = '\r\n'

DEFAULT_HTTP_VERSION = 'HTTP/1.1'

badResponseHeaders = [('Server', 'Python Thread-pool Server'),
                 ('Date', datetime.now()),
                 ('Connection', 'close')]


class HttpRequest:
    def __init__(self, method, path, http_version, headers, body, error):
        self.method = method
        self.path = urlparse(path).path
        self.http_version = http_version
        self.headers = headers
        self.body = body
        self.error = error


class HttpResponse:
    def __init__(self, code, status, headers=None, body=None):
        self.code = code
        self.status = status
        self.headers = headers
        self.body = body


class RequestParser(object):
    def __parse_request_line(self, request_line):
        request_parts = request_line.split(' ')
        self.error = 0
        if len(request_parts) != 3:
            self.error = 1
            self.method = ""
            self.url = ""
            self.protocol = ""
            return
        self.method = request_parts[0]
        self.url = request_parts[1]
        self.protocol = request_parts[2] if len(request_parts) > 2 else DEFAULT_HTTP_VERSION

    def __init__(self, req_text):
        req_lines = req_text.split(CRLF)
        self.__parse_request_line(req_lines[0])
        ind = 1
        self.headers = dict()
        while ind < len(req_lines) and len(req_lines[ind]) > 0:
            colon_ind = req_lines[ind].find(':')
            if colon_ind == -1:
                break
            header_key = req_lines[ind][:colon_ind]
            header_value = req_lines[ind][colon_ind + 1:]
            self.headers[header_key] = header_value
            ind += 1
        self.data = req_lines[ind+1:] if ind < len(req_lines) else None

    def to_request(self):
        req = HttpRequest(method=self.method,
                          path=self.url,
                          headers=self.headers,
                          http_version=self.protocol,
                          body=self.data,
                          error=self.error,)
        return req


def response(conn, res):
    resp = conn.makefile('w')
    resp.write(f'HTTP/1.1 {res.code} {res.status}\r\n')

    if res.headers:
        for (key, value) in res.headers:
            resp.write(f'{key}: {value}\r\n')
    resp.write('\r\n')

    if res.body:
        resp.write(res.body)
    resp.close()
    conn.close()


def ResponseForStatusOK(conn, path):
    type, _ = mimetypes.guess_type(path)
    headers = [('Content-Type', type),
               ('Content-Length', os.path.getsize(path)),
               ('Server', 'Python Thread-pool Server'),
               ('Date', datetime.now()),
               ('Connection', 'close')]
    response(conn, HttpResponse(200, 'OK', headers))
