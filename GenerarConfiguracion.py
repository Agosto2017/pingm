# -*- coding: utf-8 -*-
# GenerarConfiguracion.py
# pingm.py
""" Hace ping a un conjunto de equipos
"""
# 18 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0


def GenerarConfiguracion(p, p_estado, rango):
    time_stamp = '0:00:00'
    p.add_section('configuracion')
    p.add_section('Equipos')
    p_estado.add_section('estado')
    p_estado.add_section('time_stamp')
    p.set("configuracion", "arranque", "Arranque")
    p.set("configuracion", "activo", "Activo")
    p.set("configuracion", "caido", "Caido_")
    p.set("configuracion", "tiempo", "1")
    p.set("configuracion", "reintentos", "0")
    p.set("configuracion", "ayuda", "ayuda")
    for i in range(1, 256):
        p.set("Equipos", "Equipo_" + str(i), rango + str(i))
        p_estado.set("estado", "Equipo_" + str(i), 'desconocido')
        p_estado.set("time_stamp", "Equipo_" + str(i), time_stamp)
    with open("pingm.ini", "w") as f:
        p.write(f)
    with open("estado.ini", "w") as f:
        p_estado.write(f)
