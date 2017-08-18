<<<<<<< HEAD
# -*- coding: utf-8 -*-
# getiprange.py
""" Hace ping a un conjunto de equipos
"""
# 17 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import socket


def getiprange():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    a = host_ip.split(".", 3)[0:3]
    b = ".".join(a) + "."
    return b


if __name__ == "__main__":
    print getiprange()
=======
# -*- coding: utf-8 -*-
# getiprange.py
""" Hace ping a un conjunto de equipos
"""
# 17 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import socket


def getiprange():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    a = host_ip.split(".", 3)[0:3]
    b = ".".join(a) + "."
    return b


if __name__ == "__main__":
    print getiprange()
>>>>>>> 4bef55164a8691197280ac77a1d1a703914ebcd7
