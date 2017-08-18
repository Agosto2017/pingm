<<<<<<< HEAD
# -*- coding: utf-8 -*-
# log.py
""" Genera un fichero log
"""
# 17 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import time
import os


def log(msg):
    d = time.strftime("%d/%m/%Y") + " "
    t = time.strftime("%H:%M:%S") + " "
    file = time.strftime("%Y%m%d") + ".log"
    comando = "echo " + d + t + msg + " >> " + file
    # print comando,"......."
    os.system(comando)


if __name__ == '__main__':
    log("test")
