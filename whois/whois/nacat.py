#!/usr/bin/env python3.6
"""
Connect a socket, send data, and receive a response. Assemble and decode the
response and return it as string.

Assemble data for a whois.cymru.com API query.
"""
__date__ = '2017-11-14'
__version__ = (0,0,1)


import socket

def nacat(hostname, port, msg, encoding='utf-8'):
    """Send *msg* to *hostname*, *port* over a socket, and return the
    decoded response as a string."""
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect((hostname, port))
    _socket.sendall(msg.encode(encoding))
    # If trouble, uncomment and sleep(0.5) before calling shutdown.
    #_socket.shutdown(socket.SHUT_WR)

    reply = []
    while True:
        data = _socket.recv(1024)
        if not data: break
        reply.append(data)
    _socket.close()

    # More efficient to collect all the recvs in a list of bytes, and then
    # join the bytes first, then decode.
    return b''.join(reply).decode(encoding)


def join_msg(*args):
    """Return *args* as a string, prefixed with 'begin' and 'end',
    as per the whois.cymru.com API."""
    return '\n'.join(args).join(['begin\n', '\nend'])

def join_msg_from(fpath):
    """Return the lines of a file as a string, prefixed with 'begin'
    and 'end', as per the whois.cymru.com API."""
    with open(fpath, mode='r', encoding='utf-8') as f:
        return join_msg(*f.readlines())
