# file.py


def guardar_fichero(p_estado, filename='estado.ini'):
    with open(filename, 'wt') as configfile:
        p_estado.write(configfile)
