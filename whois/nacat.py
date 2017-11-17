#!/usr/bin/env python3.6

__date__ = '2017-11-14'
__version__ = (0,0,1)

"""
Connect a socket, send data, and receive a response. Assemble and decode the
response and return it as string.

Assemble data for a whois.cymru.com API query.
"""

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


#if __name__ == '__main__':
#    trgts = 'tests/samples-micro/nacat-input'
#    print(nacat( hostname='whois.cymru.com', port=43, msg=join_msg_from(trgts)), end='')
#
#    output_sample = \
#    """\
#    4134    | 49.115.196.115   | CHINANET-BACKBONE No.31,Jin-rong Street, CN
#    6429    | 190.54.22.67     | Telmex Chile Internet S.A., CL
#    9824    | 42.150.199.253   | JTCL-JP-AS Jupiter Telecommunication Co. Ltd, JP
#    9121    | 88.232.135.150   | TTNET, TR
#    4837    | 111.165.176.83   | CHINA169-BACKBONE CHINA UNICOM China169 Backbone, CN
#    34610   | 85.11.20.254     | RIKSNET, SE
#    39651   | 151.177.2.53     | COMHEM-SWEDEN, SE
#    28573   | 201.80.242.216   | CLARO S.A., BR
#    25133   | 109.227.67.186   | MCLAUT-AS, UA
#    2527    | 182.170.157.57   | SO-NET So-net Entertainment Corporation, JP
#    4837    | 121.20.254.86    | CHINA169-BACKBONE CHINA UNICOM China169 Backbone, CN
#    """
