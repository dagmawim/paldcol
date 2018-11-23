#!/usr/bin/env python

import socket

SUCCESS = 'success'
SERVER_ERROR = 'server'
CLIENT_ERROR = 'client'


def connect_to_padcol_server(command):
    client = None
    connected = False

    if len(command) != 2:
        print "[!!] Incorrect length of arguments to connect command"
        return client, connected

    try:
        ip = command[0]
        port = int(command[1])

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        print "[X] Connection established %s:%d" % (ip, port)
        connected = True
    except:
        print "[!!] Could not connect to server, check to see if server is up and ip and port are correct"

    return client, connected


def handle_response(data):
    response = data.split(',')
    return response


def parse_command(command):
    return command.split(' ')


def run_command(command, client, is_connected):
    if is_connected:
        client.send(command)
        response = handle_response(client.recv(2048))
        return response
    else:
        return CLIENT_ERROR, "[!!] No connection established..."


def run_once(is_connected, args):
    if is_connected:
        print "[!!] Persistent connection already established, terminate before proceeding"
        return
    elif len(args) < 4:
        print "[!!] Incorrect number of arguments to once command"
        return
    else:
        ip = args[0]
        port = args[1]
        client, connected = connect_to_padcol_server([ip, port])
        if not connected:
            print "[!!] Could not connect..."
        else:
            run(args[2:], client, connected)
            term_connection(connected, client)


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
            echo [item] : prints out the supplied item command
            check [item] [item] .. : checks if the supplied items are palindromes, if yes stores them
            state [option]:
                    option == num  : return the number of palindromes found so far
                    option == list : returns a list of palindromes found so far
                    option == last : returns the last element that is a palindrome
            del [index]:
                    index >= 0  : deletes the palindrome at that specified location
                    index == -1 : deleted everything in the palindrome database
            help : prints usage
            term : terminates the current connection with a paldcol server
            exit : exits the paldcol cli
    """


def run(command, client, is_connected):
    response = run_command(' '.join(command), client, is_connected)
    status = response[0]
    data = ','.join(response[1:])
    if status == SUCCESS:
        print "[X] response ==> ", data
    else:
        print "error ==> ", data



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
            client, is_connected = connect_to_padcol_server(command[1:])
        elif command[0] == "help":
            print_usage()
        elif command[0] == 'once':
            run_once(is_connected, command[1:])
        elif command[0] == "exit":
            exit_cli(is_connected, client)
        else:
            run(command, client, is_connected)


if __name__ == "__main__":
    main()
