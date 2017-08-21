# -*- coding: utf-8 -*-
# getarp.py
""" Hace ping a un conjunto de equipos
"""
# 21 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import ConfigParser
import os
import time
from file import guardar_fichero
from getos import is_windows

def GenerarConfiguracion(p_mac):
    try:
        p_mac.add_section("mac")
    except ConfigParser.DuplicateSectionError:
        pass
    guardar_fichero(p_mac, 'mac.ini')


def getarp(ip):
    p_mac = ConfigParser.RawConfigParser()
    p_mac.read("mac.ini")
    try:
        p_mac.options('mac')
    except ConfigParser.NoSectionError:
        GenerarConfiguracion(p_mac)
    try:
        mac = p_mac.get("mac", ip)
    except ConfigParser.NoOptionError:
        mac = None
    if not mac:
        if is_windows is True:
            os.system("ping -n 1 %s >NULL" % ip)
            os.system("arp -a %s >getarp.txt" % ip)
        else:
            os.system("ping -c 1 %s >NULL" % ip)
            os.system("arp -a %s >getarp.txt" % ip)
        with open('getarp.txt', 'rt') as f:
            try:
                l1 = f.readlines()
                if is_windows is True:
                    r = l1[3].split()[1].replace("-", ":")
                else:
                    r = l1[0].split()[3]
            except IndexError:
                r = "00" + ":00" * 5
            p_mac.set("mac", ip, r)
            guardar_fichero(p_mac, 'mac.ini')
    else:
        r = mac
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
                na = getarp(ip)
                print ho, ip, na


if __name__ == '__main__':
    if "all" in (os.sys.argv[1]):
        Activas()
    else:
        print getarp(os.sys.argv[1])
