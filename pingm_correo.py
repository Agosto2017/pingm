#!/usr/bin/python
#    -*-    coding:    utf-8    -*-
import ConfigParser
import time
import os
# sys.path.append("./SendMail")
from SendMail import send_email


def send_correo(origen_correo, destinatario, asunto, mensaje1):
    mensaje = []
    mensaje.append("-" * 50 + "\r\n")
    mensaje.append(mensaje1)
    mensaje.append("-" * 50 + "\r\n")
    send_email(origen_correo, destinatario, asunto, mensaje)


def ayuda():
    print("Este programa comprobar la ip")
    print("indicada en el fichero.ini")
    print("cada el tiempo en segundos indicado")
    print("enviando un correo cuando arranque")
    print("enviando un correo cuando no conteste")
    print("enviando otro correo cuando conteste")


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


def log(msg):
    d = time.strftime("%d/%m/%Y") + " "
    t = time.strftime("%H:%M:%S") + " "
    file = time.strftime("%Y%m%d") + ".log"
    comando = "echo " + d + t + msg + " >> " + file
    print comando
    os.system(comando)


def principal():
    log("Principal")
    parse = ConfigParser.RawConfigParser()
    parse_estado = ConfigParser.RawConfigParser()
    parse.read("pingm_correo.ini")
    parse_estado.read("estado.ini")
    servidorm = []
    estadom = dict()
    caidasm = dict()
    nombre = dict()
    time_stampm = dict()
    lista = parse.options('configuracion')
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
    asunto = dict()
    asunto['arranque'] = parse.get('configuracion', 'arranque')
    asunto['activo'] = parse.get('configuracion', 'activo')
    asunto['caido'] = parse.get('configuracion', 'caido')
    mensaje = parse.get('configuracion', 'mensaje')
    if not parse.get("configuracion", "saludo") == "NO":
        send_correo(origen, destinatario, asunto['arranque'], mensaje)
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
                        send_correo(origen, destinatario,
                                    asunto['activo'] + " " + nombre[servidor] +
                                    " " +
                                    servidor,
                                    mensaje)
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
                            send_correo(origen, destinatario,
                                        asunto['caido'] + " " +
                                        nombre[servidor] +
                                        " " +
                                        servidor + " ",
                                        mensaje)
            time.sleep(1)


if __name__ == "__main__":
    principal()
