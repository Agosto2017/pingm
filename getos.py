# -*- coding: utf-8 -*-
# GetOs.py
""" Obtiene operating System
"""
# 18 de Agosto de 2017
# Luis Angel Lopez
# Version 1.0


import platform

os = platform.system()
is_windows = True if "Windows" in os else False

if __name__ == '__main__':
	print is_windows