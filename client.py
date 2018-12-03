#!/usr/bin/env python

import socket

'''
Status codes
'''
SUCCESS = 'success'
SERVER_ERROR = 'server'
CLIENT_ERROR = 'client'


def connect_to_padcol_server(command):
    '''
    used a socker to connect to a paldcol server
    :param command:
    :return:
    '''
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


def run_command(command, client, is_connected):
    '''
    runs the command through the client connection, if
    the connection has been established

    :param command:
    :param client:
    :param is_connected:
    :return:
    '''
    if is_connected:
        client.send(command)
        response = client.recv(2048).split(',')
        return response
    else:
        return CLIENT_ERROR, "[!!] No connection established..."


def run_once(is_connected, args):
    '''
    Do not create a persistent connection but only run a command once
    and close the connection
    :param is_connected:
    :param args:
    :return:
    '''
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
    '''
    function to abstract the tasks required to close a connection
    :param is_connected:
    :param client:
    :return:
    '''
    if is_connected:
        print "Closing connection with %s:%d..." % client.getsockname()
        client.send('term')
        client.close()
    else:
        print "[!!] No connection to terminate..."


def exit_cli(is_connected, client):
    '''
    exit the cli when user types 'exit'
    :param is_connected:
    :param client:
    :return:
    '''
    term_connection(is_connected, client)
    print "bye bye..."
    exit(0)


def print_usage():
    '''
    Prints the usage string
    :return:
    '''
    print """  
    paldcol protocol usage:
            connect [ip] [port] : connects with a paldcol server listening on this ip, port
            once [ip] [port] [normal arg] : runs a command in a non-persistent connection. normal arg is
                some other command in this list.  
            echo [item] : prints out the supplied item
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
    '''
    Run the application for paldcol
    :param command:
    :param client:
    :param is_connected:
    :return:
    '''
    response = run_command(' '.join(command), client, is_connected)
    status = response[0]
    data = ','.join(response[1:])
    if status == SUCCESS:
        print "[X] response ==> ", data
    else:
        print "error ==> ", data


def main():
    '''
    Main function to run and connect to a paldcol server
    :return:
    '''
    prompt = "$ paldcol : "
    is_connected = False
    client = None

    while True:
        command = raw_input(prompt).split(' ')

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
