#!/usr/bin/env python

import socket
from threading import Thread
import json

SUCCESS = 'success'
SERVER_ERROR = 'server'
CLIENT_ERROR = 'client'
STORAGE_FILE = './storage.json'


class Client(Thread):

    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        print "[+] client connected at %s:%d" % (ip,port)

    def close_connection(self):
        print "closing connection from %s:%d" % (self.ip, self.port)
        self.conn.shutdown(socket.SHUT_RD | socket.SHUT_WR)
        self.conn.close()
        exit()

    @staticmethod
    def run_state(args):
        if len(args) == 0:
            return CLIENT_ERROR, "[!!] Number of arguments supplied is incorrect"

        with open(STORAGE_FILE, 'r') as file:
            db = json.load(file)
            if args[0] == "num":
                result = str(len(db))
            elif args[0] == "list":
                result = ','.join([word['word'] for word in db])
            elif args[0] == "last":
                if len(db) != 0:
                    result = str(db[-1]['word'])
                else:
                    return SERVER_ERROR, "[!!] No items currently in storage"
            else:
                return CLIENT_ERROR, "[!!] Incorrect arg to state command"

        return SUCCESS, result

    @staticmethod
    def run_del(args):
        if len(args) != 1:
            return CLIENT_ERROR, "[!!] Number of arguments supplied is incorrect"

        with open(STORAGE_FILE, 'r') as file:
            db = json.load(file)
            for arg in args:
                del_index = int(arg)
                if del_index == -1:
                    db = []
                elif del_index < len(db):
                    del db[del_index]
                else:
                    return SERVER_ERROR, "[!!] Index supplied not in range"

        with open(STORAGE_FILE, 'w') as file:
            json.dump(db, file)

        return SUCCESS, '[X] Deleted value at index : ' + ' '.join(args)

    @staticmethod
    def run_check(words):
        if len(words) == 0:
            return CLIENT_ERROR, "[!!] Number of arguments supplied is incorrect"

        result = ''
        with open(STORAGE_FILE, 'r') as file:
            db = json.load(file)
            print "checking words...", words
            for word in words:
                if word == word[::-1]:
                    result += '1,'
                    db.append({
                        'word': word
                    })
                else:
                    result += '0,'
        print "Updating storage with new palindromes"
        with open(STORAGE_FILE, 'w') as file:
            json.dump(db, file)

        print result[:-1]
        return SUCCESS, result[:-1]

    @staticmethod
    def parse_request(request):
            return request.split(' ')

    def handle_command(self, request):
        print "server received command: '%s' from %s:%d" % (request, self.ip, self.port)
        command = self.parse_request(request)
        if command[0] == 'term':
            self.close_connection()
            return SUCCESS, "closed"
        elif command[0] == "echo":
            return SUCCESS, ' '.join(command[1:])
        elif command[0] == 'check':
            words = command[1:]
            return self.run_check(words)
        elif command[0] == 'state':
            args = command[1:]
            return self.run_state(args)
        elif command[0] == 'del':
            args = command[1:]
            return self.run_del(args)
        else:
            return CLIENT_ERROR, "[!!] paldcol command not recognized"

    def run(self):
        while True:
            status, response = self.handle_command(self.conn.recv(2048))
            full_response = str(status) + ',' + str(response)
            # print "sending...", full_response
            self.conn.send(full_response)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    max_clients = 10
    while True:
        server.listen(max_clients)
        print "listening for connections from paldcol clients..."
        (conn, (ip, port)) = server.accept()
        new_client = Client(ip, port, conn)
        new_client.start()


if __name__ == '__main__':
    main()




