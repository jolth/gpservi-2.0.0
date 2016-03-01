# -*- coding: UTF-8 -*-
"""
Aplicacion para localizar coordenadas GPS en formato UTM WGS84, DMS y Decimales.
"""

def latWgs84ToDecimal(lat):
	lat = list(lat)
	lat.insert(3, '.')
	lat = "".join(lat).partition('.')
	return "%s%s%s" % (int(lat[0]), lat[1], lat[2])



def lngWgs84ToDecimal(lng):
	lng = list(lng)
	lng.insert(4, '.')
	lng = "".join(lng).partition('.')
	return "%s%s%s" % (int(lng[0]), lng[1], lng[2])


