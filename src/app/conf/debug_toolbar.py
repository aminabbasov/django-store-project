import socket


INTERNAL_IPS = [
    "127.0.0.1",
]

# to enable a toolbar with docker
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
