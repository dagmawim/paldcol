# Python TCP Client A
import socket


def connect_to_padcol_server(command):
    client = None
    connected = False

    if len(command) != 3:
        print "[!!] Incorrect length of arguments to connect command"
        return client, connected

    ip = command[1]
    port = int(command[2])

    print "Connecting to server at %s:%d..." % (ip, port)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        print "[X] Connection established"
        connected = True
    except:
        print "[!!] Could not connect to server %s:%d, check to see if server is up" % (ip, port)

    return client, connected


def handle_response(data):
    print "[=>] received data:", data


def parse_command(command):
    return command.split(' ')


def run_command(command, client):
    client.send(command)
    buffer_size = 2048
    data = client.recv(buffer_size)
    return handle_response(data)


def term_connection(is_connected, client):
    if is_connected:
        print "Closing connection with %s:%d..." % client.getsockname()
        client.send('term')
        client.close()
    else:
        print "[!!] No connection to terminate..."


def exit_cli(is_connected, client):
    term_connection(is_connected, client)
    print "bye bye..."
    exit(0)


def print_usage():
    print """  
    paldcol protocol usage:
            connect [ip] [port] : connects with a paldcol server listening on this ip, port
            help : prints usage
            term : terminates the current connection with a paldcol server
            exit : exits the paldcol cli
    """


def main():
    prompt = "$ paldcol : "
    is_connected = False
    client = None

    while True:
        command = parse_command(raw_input(prompt))

        if command[0] == 'term':
            term_connection(is_connected, client)
            client = None
            is_connected = False
        elif command[0] == "connect":
            client, is_connected = connect_to_padcol_server(command)
        elif command[0] == "help":
            print_usage()
        elif command[0] == "exit":
            exit_cli(is_connected, client)
        else:
            print "[!!] paldcol command not recognized"


if __name__ == "__main__":
    main()
