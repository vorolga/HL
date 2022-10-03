from server import run_server

from utils import parse

if __name__ == '__main__':
    thread_limit, document_root, host, port = parse()
    run_server(thread_limit, document_root, host, port)
