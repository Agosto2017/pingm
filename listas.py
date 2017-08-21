# listas
import time
from getname import getname

def Activas(estado=True):
    activas = dict()
    caidas = dict()
    file = time.strftime("%Y%m%d") + ".log"
    with open(file, 'rt') as f:
        l1 = f.readlines()
        cont = 0
        for i in l1:
            if "Activo" in i and estado is True:
                cont = cont + 1
                ho = i.split()[1]
                ip = i.split()[4][1:-1]
                if ip in activas:
                    activas[ip] = ho
                    continue
                activas[ip] = ho
                # na = getname(ip)
                # print ho, ip
            if "Caido_" in i and estado is False:
                cont = cont + 1
                ho = i.split()[1]
                ip = i.split()[4][1:-1]
                if ip in caidas:
                    caidas[ip] = ho
                    continue
                caidas[ip] = ho
                # na = getname(ip)
                # print ho, ip
    return activas, caidas


class ob:
    hi = 1
    hf = 1
    stdi = 1

    def __init__(self):
        self.hi = 1
        self.hf = 1
        self.stdi = 1
        pass


def activasycaidas():
    a, k = Activas(True)
    k, c = Activas(False)
    res = []
    for i in a:
        if i in c:
            if a[i] > c[i]:
                m = i + ' [' + getname(i) +\
                    ']', "caida a %s activa a %s" % (c[i], a[i])
                print m
                obj = ob()
                obj.hi = c[i]
                obj.hf = a[i]
                obj.stdi = "caida"
                res.append(obj)
            else:
                m = i + ' [' + getname(i) + ']',\
                    "activa a %s caida a %s" % (a[i], c[i])
                print m
                obj = ob()
                obj.hi = a[i]
                obj.hf = c[i]
                #obj.stdi = "Activa"
                res.append(obj)
    return res


if __name__ == '__main__':
    res = activasycaidas()
    for i in range(len(res)):
        print i,res[i].hi
        print res[i].hi, res[i].hf, res[i].stdi
