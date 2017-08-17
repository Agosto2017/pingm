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


def ayuda():
    print("Este programa comprobará la ip")
    print("indicada en el fichero.ini")
    print("cada el tiempo <indicado> en segundos")


def numberpatron(filename, patron1, patron2):
    with open(filename) as file:
        file.readlines()
        numero = 0
        for i in file:
            if patron1 in i:
                numero = numero + 1
            elif patron2 in i:
                numero = numero + 1
        return numero


def guardar_fichero(parse_estado):
    # Writing our configuration file to 'example.cfg'
    with open('estado.ini', 'wt') as configfile:
        parse_estado.write(configfile)


def GenerarConfiguracion(parse, parse_estado):
    time_stamp = '0:00:00'
    parse.add_section('configuracion')
    parse_estado.add_section('estado')
    parse_estado.add_section('time_stamp')
    parse.set("configuracion", "arranque", "Arranque")
    parse.set("configuracion", "activo", "Activo")
    parse.set("configuracion", "caido", "Caido")
    parse.set("configuracion", "tiempo", "1")
    parse.set("configuracion", "reintentos", "3")
    parse.set("configuracion", "reintentos", "3")
    parse.set("configuracion", "ayuda", "ayuda")
    for i in range(1, 254):
        parse.set("configuracion", "servidor" + str(i), getiprange() + str(i))
        parse_estado.set("estado", "servidor" + str(i), 'desconocido')
        parse_estado.set("time_stamp", "servidor" + str(i), time_stamp)
    with open("pingm.ini", "w") as f:
        parse.write(f)
    with open("estado.ini", "w") as f:
        parse_estado.write(f)


def principal():
    log("Principal")
    parse = ConfigParser.RawConfigParser()
    parse_estado = ConfigParser.RawConfigParser()
    parse.read("pingm.ini")
    parse_estado.read("estado.ini")
    servidorm = []
    estadom = dict()
    caidasm = dict()
    nombre = dict()
    time_stampm = dict()
    try:
        lista = parse.options('configuracion')
    except:
        print ("Genero configuracion")
        GenerarConfiguracion(parse, parse_estado)
        lista = parse.options('configuracion')
    else:
        for i in lista:
            # print i
            pass
        print "otro error"
    finally:
        print "fin"
    asunto = dict()
    asunto['arranque'] = parse.get('configuracion', 'arranque')
    asunto['activo'] = parse.get('configuracion', 'activo')
    asunto['caido'] = parse.get('configuracion', 'caido')
    for i in lista:
        if 'servidor' in i:
            servidor = parse.get('configuracion', i)
            servidorm.append(servidor)
            estado = ""
            try:
                estado = parse_estado.get('estado', i)
                time_stamp = parse_estado.get('time_stamp', i)
            except estado:
                estado = 'desconocido'
                time_stamp = '0:00:00'
                try:
                    parse_estado.add_section('estado')
                    parse_estado.add_section('time_stamp')
                except parse_estado:
                    estado = 'desconocido'
                    time_stamp = '00:00:00'
            parse_estado.set('estado', i, estado)
            parse_estado.set('time_stamp', i, time_stamp)
            estadom[servidor] = estado
            caidasm[servidor] = 0
            nombre[servidor] = i
            time_stampm[servidor] = time_stamp
    guardar_fichero(parse_estado)
    tiempo = parse.getint('configuracion', 'tiempo')
    reintentos = parse.getint('configuracion', 'reintentos')
    if not parse.get("configuracion", "ayuda") == "NO":
        ayuda()
    while True:
        filename = "tmp.txt"
        d = time.strftime("%d/%m/%Y") + " "
        t = time.strftime("%H:%M:%S") + " "
        if int(time.time() % tiempo) == 0:
            for servidor in servidorm:
                comando = "ping -n 3 " + servidor + "> " + filename
                os.system(comando)
                if numberpatron(filename, "agotado", "inaccesible") < 3:
                    caidasm[servidor] = 0
                    if not (estadom[servidor] == "activo"):
                        print(t + "Cambio de estado de ", estadom[servidor],
                              " a estado activo: " + nombre[servidor] + " " +
                              servidor)
                        estadom[servidor] = "activo"
                        time_stampm[servidor] = d + t
                        print "servidor", servidor
                        print "nombre[servidor]", nombre[servidor]
                        print "estado[servidor]", estadom[servidor]
                        parse_estado.set('estado', nombre[servidor],
                                         estadom[servidor])
                        parse_estado.set('time_stamp', nombre[servidor],
                                         time_stampm[servidor])
                        guardar_fichero(parse_estado)
                        log(asunto['activo'] + " " + nombre[servidor] +
                            " " +
                            servidor)
                else:
                    if not (estadom[servidor] == "caido"):
                        caidasm[servidor] = caidasm[servidor] + 1
                        if caidasm[servidor] >= reintentos:
                            print(t + "Cambio de estado de ",
                                  estadom[servidor],
                                  " a estado no_activo: " + nombre[servidor] +
                                  " " +
                                  servidor)
                            estadom[servidor] = "caido"
                            time_stampm[servidor] = d + t
                            parse_estado.set('estado', nombre[servidor],
                                             estadom[servidor])
                            parse_estado.set('time_stamp', nombre[servidor],
                                             time_stampm[servidor])
                            guardar_fichero(parse_estado)
                            log(asunto['caido'] + " " + nombre[servidor] +
                                " " +
                                servidor + " ")
            time.sleep(1)


if __name__ == "__main__":
    principal()
