from math import floor, log
from dateutil.parser import parse
from django.utils import timezone


def redo_string(dic, string1, string2=None):
    """
    Busca un valor en un diccionario o un valor dentro de otro. Si no lo encuentra, devuelve una cadena vacía.

    :param dic:
    :param string1:
    :param string2:
    :return:
    """
    if string2:
        if string1 in dic and string2 in dic[string1]:
            return dic[string1][string2]
        else:
            return ""
    else:
        if string1 in dic:
            return dic[string1]
        else:
            return ""


def redo_date(dic, string):
    """
    Busca un valor de tipo date dentro de un diccionario y lo parsea. Si da error, devuelve una cadena vacía.

    :param dic:
    :param string:
    :return:
    """
    if string in dic:
        try:
            return timezone.localtime(parse(dic[string]))
        except Exception:
            pass

    return timezone.now()


def only_keys(dic, keys):
    return {x: dic[x] for x in dic if x in keys}


def floor_log(number):
    if number == 0:
        return 0
    else:
        return floor(log(number))
