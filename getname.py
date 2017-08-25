# -*- coding: utf-8 -*-
# getname
""" Hace ping a un conjunto de equipos
"""
# 21 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import os
import ConfigParser
import time
from file import guardar_fichero


def GenerarConfiguracion(p_name):
    try:
        p_name.add_section("name")
    except ConfigParser.DuplicateSectionError:
        pass
    guardar_fichero(p_name, 'name.ini')


def getname(ip):
    p_name = ConfigParser.RawConfigParser()
    p_name.read("name.ini")
    try:
        p_name.options('name')
    except ConfigParser.NoSectionError:
        GenerarConfiguracion(p_name)
    try:
        name = p_name.get("name", ip)
    except ConfigParser.NoOptionError:
        name = None
    if not name:
        os.system("ping -a -n 2 %s >getname.txt" % ip)
        with open('getname.txt', 'rt') as f:
            try:
                l1 = f.readlines()
                r = l1[1].split()[3]
            except IndexError:
                r = ip
            p_name.set("name", ip, r)
            guardar_fichero(p_name, 'name.ini')
    else:
        r = name
    return r


def Activas():
    file = time.strftime("%Y%m%d") + ".log"
    with open(file, 'rt') as f:
        l1 = f.readlines()
        cont = 0
        for j in range(len(l1) - 1, len(l1) - 1 and cont < 10, -1):
            i = l1[j]
            if "Activo" in i:
                cont = cont + 1
                ho = i.split()[1]
                ip = i.split()[4][1:-1]
                na = getname(ip)
                print ho, ip, na


if __name__ == '__main__':
    if "all" in (os.sys.argv[1]):
        Activas()
    else:
        print getname(os.sys.argv[1])
