# -*- coding: utf-8 -*-
# log.py
""" Genera un fichero log
"""
# 17 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import time
import os
from getname import getname


def log(msg, debug=True):
    d = time.strftime("%d/%m/%Y") + " "
    t = time.strftime("%H:%M:%S") + " "
    file = time.strftime("%Y%m%d") + ".log"
    comando = "echo " + d + t + msg + " >> " + file
    print comando
    os.system(comando)
    if debug is True:
        if "Activo" in msg:
            a = comando.split(" ")
            ip = a[5][1:-1]
            b = a[4] + " " + ip + "[" + getname(ip) + ']'
            os.system('presenta.cmd "' + b + '"')
        if "Caido" in msg:
            a = comando.split(" ")
            ip = a[5][1:-1]
            b = a[4] + " " + ip + "[" + getname(ip) + ']'
            os.system('presenta.cmd "' + b + '"')


if __name__ == '__main__':
    log("test", debug=True)
