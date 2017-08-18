# -*- coding: utf-8 -*-
# pingm.py
""" Hace ping a un conjunto de equipos
"""
# 18 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0


def GenerarConfiguracion(p, p_estado, rango):
    time_stamp = '0:00:00'
    p.add_section('configuracion')
    p_estado.add_section('estado')
    p_estado.add_section('time_stamp')
    p.set("configuracion", "arranque", "Arranque")
    p.set("configuracion", "activo", "Activo")
    p.set("configuracion", "caido", "Caido")
    p.set("configuracion", "tiempo", "1")
    p.set("configuracion", "reintentos", "0")
    p.set("configuracion", "ayuda", "ayuda")
    for i in range(1, 254):
        p.set("configuracion", "servidor" + str(i), rango + str(i))
        p_estado.set("estado", "servidor" + str(i), 'desconocido')
        p_estado.set("time_stamp", "servidor" + str(i), time_stamp)
    with open("pingm.ini", "w") as f:
        p.write(f)
    with open("estado.ini", "w") as f:
        p_estado.write(f)
