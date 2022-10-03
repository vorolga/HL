import multiprocessing
import os
import queue
import signal
import socket
import threading
from handler import handle


class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


class ThreadPoolManger():
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


def run_server(thread_limit, document_root, host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server started on", host, ":", port)

    cpu_count = multiprocessing.cpu_count()

    pids = []
    try:
        for thread in range(cpu_count):
            pid = os.fork()

            if pid != 0:
                print('Новый дочерний процесс: ', pid)
                pids.append(pid)
                thread_pool = ThreadPoolManger(thread_limit)
                while True:
                    sock, addr = server_socket.accept()
                    thread_pool.add_work(handle, *(sock, document_root))
    except KeyboardInterrupt:
        server_socket.close()
        for pid in pids:
            print("killing ", pid)
            os.kill(pid, signal.SIGTERM)
        print("server down")
