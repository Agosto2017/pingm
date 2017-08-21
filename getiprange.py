# -*- coding: utf-8 -*-
# getiprange.py
""" Hace ping a un conjunto de equipos
"""
# 17 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import os
import socket
from getos import is_windows


def getiprange():
    if is_windows is True:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        a = host_ip.split(".", 3)[0:3]
        b = ".".join(a) + "."
        return b
    else:
        os.system("ifconfig eth0 >ifconfig.txt")
        with open("ifconfig.txt", 'rt') as f:
            l1 = f.readlines()
            a = l1[1].split(':')[1].split()[0].split(".",3)[0:3]
            b = ".".join(a) + "."
        return b


if __name__ == "__main__":
    print getiprange()
