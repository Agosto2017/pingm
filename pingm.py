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


def ayuda():
    print("Este programa comprobar la ip")
    print("indicada en el fichero.ini")
    print("cada el tiempo en segundos indicado")


def numberpatron(filename, patron1, patron2):
    file = open(filename).readlines()
    numero = 0
    for i in file:
        if patron1 in i:
            numero = numero + 1
        if patron2 in i:
            numero = numero + 1
    return numero


def guardar_fichero(parse_estado):
    # Writing our configuration file to 'example.cfg'
    with open('estado.ini', 'wt') as configfile:
        parse_estado.write(configfile)


def GenerarConfiguracion(parse):
    parse.add_section('configuracion')
    for i in range(1, 254):
        parse.set("configuracion", "servidor" + str(i), "192.168.1." + str(i))
    with open("pingm.ini", "w") as f:
        parse.write(f)


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
    except lista:
        print ("Genero configuracion")
        GenerarConfiguracion(parse)
        return
    for i in lista:
        if 'servidor' in i:
            print i
            servidor = parse.get('configuracion', i)
            servidorm.append(servidor)
            try:
                estado = parse_estado.get('estado', i)
                time_stamp = parse_estado.get('time_stamp', i)
                print estado
            except:
                estado = 'desconocido'
                time_stamp = '0:00:00'
                try:
                    parse_estado.add_section('estado')
                    parse_estado.add_section('time_stamp')
                except:
                    estado = 'desconocido'
                    time_stamp = '00:00:00'
            parse_estado.set('estado', i, estado)
            parse_estado.set('time_stamp', i, time_stamp)
            estadom[servidor] = estado
            caidasm[servidor] = 0
            nombre[servidor] = i
            time_stampm[servidor] = time_stamp
    guardar_fichero(parse_estado)
    origen = parse.get('configuracion', 'origen')
    tiempo = parse.getint('configuracion', 'tiempo')
    destinatario = parse.get('configuracion', 'destinatario')
    reintentos = parse.getint('configuracion', 'reintentos')
    if not parse.get("configuracion", "ayuda") == "NO":
        ayuda()
    while True:
        filename = "tmp.txt"
        d = time.strftime("%d/%m/%Y") + " "
        t = time.strftime("%H:%M:%S") + " "
        if int(time.time() % tiempo) == 0:
            for servidor in servidorm:
                print servidor
                comando = "ping -n 3 " + servidor + "> " + filename
                os.system(comando)
                print comando
                if numberpatron(filename,"agotado","inaccesible") < 3:
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
