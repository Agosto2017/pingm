# -*- coding: utf-8 -*-
# pingm.py
""" Hace ping a un conjunto de equipos
"""
# 17 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0

import ConfigParser
import time
import os
from log import log as log
from getiprange import getiprange as getiprange
from getos import is_windows
from GenerarConfiguracion import GenerarConfiguracion as gc


def ayuda(tiempo):
    print("Este programa comprobará la ip\n"
          "indicada en el fichero.ini\n"
          "cada el tiempo <%d> en segundos\n" % tiempo)


def numberpatron(filename, patrones):
    with open(filename) as f:
        fi = f.readlines()
        n = 0
        for i in fi:
            for patron in patrones:
                n = n + 1 if patron in i else n
        return n


def guardar_fichero(p_estado):
    with open('estado.ini', 'wt') as configfile:
        p_estado.write(configfile)


def principal():
    log("Principal")
    p = ConfigParser.RawConfigParser()
    p_estado = ConfigParser.RawConfigParser()
    p.read("pingm.ini")
    p_estado.read("estado.ini")
    eqm = []
    stdm = dict()
    caidasm = dict()
    name = dict()
    time_stampm = dict()
    try:
        lista = p.options('Equipos')
    except ConfigParser.NoSectionError:
        print ("Genero configuracion")
        gc(p, p_estado, getiprange())
        lista = p.options('Equipos')
    finally:
        pass
    sbj = dict()
    sbj['arranque'] = p.get('configuracion', 'arranque')
    sbj['activo'] = p.get('configuracion', 'activo')
    sbj['caido'] = p.get('configuracion', 'caido')
    for i in lista:
        eq = p.get('Equipos', i)
        eqm.append(eq)
        estado = ""
        try:
            estado = p_estado.get('estado', i)
            time_stamp = p_estado.get('time_stamp', i)
        except ConfigParser.NoSectionError:
            p_estado.add_section('time_stamp')
            time_stamp = '0:00:00'
        except ConfigParser.NoOptionError:
            p_estado.set('time_stamp', i, time_stamp)
        except estado:
            estado = 'desconocido'
            time_stamp = '0:00:00'
            try:
                p_estado.add_section('estado')
                p_estado.add_section('time_stamp')
            except p_estado:
                estado = 'desconocido'
                time_stamp = '00:00:00'
        p_estado.set('estado', i, estado)
        p_estado.set('time_stamp', i, time_stamp)
        stdm[eq] = estado
        caidasm[eq] = 0
        name[eq] = i
        time_stampm[eq] = time_stamp
    guardar_fichero(p_estado)
    tiempo = p.getint('configuracion', 'tiempo')
    reintentos = p.getint('configuracion', 'reintentos')
    if not p.get("configuracion", "ayuda") == "NO":
        ayuda(tiempo)
    while True:
        filename = "tmp.txt"
        if int(time.time()) % tiempo == 0:
            for eq in eqm:
                d = time.strftime("%d/%m/%Y") + " "
                t = time.strftime("%H:%M:%S") + " "
                if is_windows:
                    comando = "ping -n 3 " + eq + "> " + filename
                else:
                    comando = "ping -c 3 " + eq + "> " + filename
                print "Revisando", eq
                os.system(comando)
                if numberpatron(filename, ("agotado", "inaccesible", "Unreachable")) < 3:
                    caidasm[eq] = 0
                    if not (stdm[eq] == "activo"):
                        print(t + "Cambio de estado de ", stdm[eq],
                              " a estado activo: " + name[eq] + " " +
                              eq)
                        stdm[eq] = "activo"
                        time_stampm[eq] = d + t
                        print "eq", eq
                        print "name[eq]", name[eq]
                        print "estado[eq]", stdm[eq]
                        p_estado.set('estado', name[eq],
                                     stdm[eq])
                        p_estado.set('time_stamp', name[eq],
                                     time_stampm[eq])
                        guardar_fichero(p_estado)
                        print "escribo log"
                        log(name[eq] + " " + sbj['activo'] + " (" + eq + ")")
                else:
                    if not (stdm[eq] == "caido"):
                        caidasm[eq] = caidasm[eq] + 1
                        if caidasm[eq] >= reintentos:
                            print(t + "Cambio de estado de ", stdm[eq],
                                  " a estado no_activo: " + name[eq] + " " +
                                  eq)
                            stdm[eq] = "caido"
                            time_stampm[eq] = d + t
                            p_estado.set('estado', name[eq],
                                         stdm[eq])
                            p_estado.set('time_stamp', name[eq],
                                         time_stampm[eq])
                            guardar_fichero(p_estado)
                            log(name[eq] + " " + sbj['caido'] +
                                " (" + eq + ")")
            time.sleep(1)


if __name__ == "__main__":
    principal()
