# -*- coding: utf-8 -*-
# Author: Jorge A. Toro
# URL OSM: http://nominatim.openstreetmap.org/reverse?format=json&lon=-75.51738&addressdetails=1&zoom=18&lat=5.06889&email=jorge.toro%40devmicrosystem.com
"""
    Geocoding API Google/OSM

    Usage: 
        >>> import geocoding
        >>>
        >>> geocoding.geocodeGMap('Manizales')
        '["Manizales, Caldas, Colombia", "Manizales, Caldas, Colombia"]'
        >>>
        >>> geocoding.regeocodeGMap('5.06889,-75.51738')
        '["Carrera 20 # 22-1 a 22-99, Manizales, Caldas, Colombia", "Manizales, Caldas, Colombia", "Caldas, Colombia", "Colombia"]'
        >>>
"""
import urllib, json

#GEOCODE_BASE_URL = 'http://maps.google.com/maps/api/geocode/json'
GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
REGEOCODE_BASE_URL = 'http://maps.google.com/maps/geo'
OSM_REGEOCODE_BASE_URL = 'http://nominatim.openstreetmap.org/reverse'
MAPQ_REGEOCODE_BASE_URL = 'http://open.mapquestapi.com/nominatim/v1/reverse.php'

def geocodeGMap(address, sensor='false', **geo_args):
    """
        Geocoding Google Map
    """
    geo_args = ({
        'address': address,
        'sensor': sensor
    })

    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = json.load(urllib.urlopen(url))
    return json.dumps([s['formatted_address']
                       for s in result['results']])

def regeocodeGMapOLD(latlng, sensor='false', **geo_args):
    """
        Google Map Reverse Geocoding 
        URL: http://maps.google.com/maps/geo?q=5.06889,-75.51738&output=json&sensor=false
    """
    geo_args = ({
        'key' : 'AIzaSyBPqUNglpVE274TVIWSbk1cPLsJTKDTfa8',
        'q' : latlng,
        'output' : 'json',
        'sensor' : sensor
    })

    url = REGEOCODE_BASE_URL + '?' + urllib.unquote(urllib.urlencode(geo_args))
    #print url
    result = json.load(urllib.urlopen(url))

    return json.dumps([s['address'] 
               for s in result['Placemark']])


def regeocodeGMap(latlng, level=None, sensor='false', **geo_args):
    """
        Google Map Reverse Geocoding
            
            Por defecto level se pone a 0. Lo cual nos muestra la 
            ubicación con el maximo detalle.

        Usage:
            >>> geocoding.regeocodeGMap('5.06889,-75.51738')
            u'Carrera 20 # 22-1 a 22-99, Manizales, Caldas, Colombia'
            >>> geocoding.regeocodeGMap('5.06889,-75.51738', 1)
            u'Manizales, Caldas, Colombia'
            >>> geocoding.regeocodeGMap('5.06889,-75.51738', 2)
            u'Caldas, Colombia'
            >>> geocoding.regeocodeGMap('5.06889,-75.51738', 3)
            u'Colombia'
            >>>
    """
    geo_args = ({
        'latlng' : latlng,
        'sensor' : sensor
    })

    url = GEOCODE_BASE_URL + '?' + urllib.unquote(urllib.urlencode(geo_args))
    #print url
    result = json.load(urllib.urlopen(url))
    return level and json.loads(json.dumps([s['formatted_address'] 
           for s in result['results']]))[level] or json.loads(json.dumps([s['formatted_address']
               for s in result['results']]))[0]


def regeocodeOSM(latlng, **geo_args):
    """
        OSM Reverse Geocoding

        usage:
        >>> geocoding.regeocodeOSM('5.03515676667,-75.4606770833')
        u'50, Parque Industrial Juanchito, Tesorito, Comuna Tesorito, Manizales, Centrosur, Caldas, 170003, Colombia'
        >>>
    """
    latlng = latlng.split(',')

    geo_args = ({
        'format' : 'json',
        'lat'  : latlng[0],
        'lon' : latlng[1],
        'zoom'  : 18,
        'addressdetails'  : 1,
        #'email'  : 'jorge.toro@devmicrosystem.com'.encode("utf8")
    })

    #url = OSM_REGEOCODE_BASE_URL + '?' + urllib.unquote(urllib.urlencode(geo_args))
    url = MAPQ_REGEOCODE_BASE_URL + '?' + urllib.unquote(urllib.urlencode(geo_args))

    #print url
    result = json.load(urllib.urlopen(url))
    #print result
    #return json.dumps([s['address'] 
    #                   for s in result['Placemark']])

    #return result['address']

    #address = result['address']
    #return "%s, %s, %s, " % (address['public_building'], address['road'], address['neighbourhood'], 
    #        address[''], address[''])

    return result['display_name']

