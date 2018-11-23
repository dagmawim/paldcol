import socket
from threading import Thread


class Client(Thread):
    success = 'success'

    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        print "[+] client connected at %s:%d" % (ip,port)

    def handle_command(self, request):
        print "server received data: %s from %s:%d" % (request, self.ip, self.port)
        if request == 'term':
            print "closing connection from %s:%d" % (self.ip, self.port)
            self.conn.shutdown(socket.SHUT_RD | socket.SHUT_WR)
            self.conn.close()
            exit()
        response = request
        return self.success, response

    def run(self):
        while True:
            status, response = self.handle_command(self.conn.recv(2048))
            self.conn.send(str(status) + ', ' + str(response))


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    threads = []
    max_clients = 10
    while True:
        server.listen(max_clients)
        print "listening for connections from paldcol clients..."
        (conn, (ip, port)) = server.accept()
        new_client = Client(ip, port, conn)
        new_client.start()
        threads.append(new_client)


if __name__ == '__main__':
    main()




