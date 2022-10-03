DEFAULT_THREAD_LIMIT = 256
DEFAULT_DIR = '/var/www/html'
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 80
DEFAULT_CONNECTIONS_LIMIT = 1000


def parse():
    thread_limit = DEFAULT_THREAD_LIMIT
    document_root = DEFAULT_DIR
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    connections_limit = DEFAULT_CONNECTIONS_LIMIT

    try:
        file = open('httpd.conf', 'r')
    except:
        return thread_limit, document_root, host, port

    text = file.read().split()
    i = 1
    for word in text:
        if word == 'thread_limit':
            thread_limit = int(text[i])
        elif word == 'document_root':
            document_root = text[i]
        elif word == 'host':
            host = text[i]
        elif word == 'port':
            port = int(text[i])
        i += 1
    return thread_limit, document_root, host, port
