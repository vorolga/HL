from urllib.parse import unquote

import HttpReqResp


def handle(conn, document_root):
    rawFile = conn.makefile('r')
    info = rawFile.readline()
    r = HttpReqResp.RequestParser(info)

    request = r.to_request()

    if request.error == 1:
        HttpReqResp.response(conn,
                             HttpReqResp.HttpResponse(400, 'Bad request', HttpReqResp.badResponseHeaders))
        return

    if request.method != 'GET' and request.method != 'HEAD':
        HttpReqResp.response(conn,
                             HttpReqResp.HttpResponse(405, 'Method Not Allowed', HttpReqResp.badResponseHeaders))
        return

    if request.path.find('../') != -1:
        HttpReqResp.response(conn,
                             HttpReqResp.HttpResponse(403, 'Forbidden', HttpReqResp.badResponseHeaders))
        return

    indexFile = False
    unquotedPath = unquote(request.path)
    if request.path[-1] == '/' and request.path.find('.') == -1:
        filePath = document_root + unquotedPath + 'index.html'
        indexFile = True
    else:
        filePath = document_root + unquotedPath

    try:
        file = open(filePath, 'rb')
    except:
        if indexFile:
            resp = HttpReqResp.HttpResponse(
                403, 'Forbidden', headers=HttpReqResp.badResponseHeaders)
        else:
            resp = HttpReqResp.HttpResponse(
                404, 'Not Found', headers=HttpReqResp.badResponseHeaders)

        HttpReqResp.response(conn, resp)
        return

    HttpReqResp.ResponseForStatusOK(conn, filePath)
    if request.method == 'GET':
        try:
            conn.sendfile(file)
        except BrokenPipeError:
            conn.sendfile(file)
    file.close()
