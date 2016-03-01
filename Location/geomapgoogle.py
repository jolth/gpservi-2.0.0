"""
Geocoding API Google

 import geomapgoogle
 geomapgoogle.geocode('San Francisco')
 
 geomapgoogle.regeocode(latlng='40.714224,-73.961452')
 
"""
import urllib, json

#GEOCODE_BASE_URL = 'http://maps.google.com/maps/api/geocode/json'
GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
REGEOCODE_BASE_URL = 'http://maps.google.com/maps/geo'
OSM_REGEOCODE_BASE_URL = 'http://nominatim.openstreetmap.org/reverse'

def geocode(address, sensor='false', **geo_args):
    """
        Geocoding
    """
    geo_args = ({
        'address': address,
        'sensor': sensor
    })

    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = json.load(urllib.urlopen(url))
    return json.dumps([s['formatted_address']
                       for s in result['results']])

def regeocodeOLD(latlng, sensor='false', **geo_args):
    """
        Reverse Geocoding
    """
    geo_args = ({
        'key' : 'AIzaSyBPqUNglpVE274TVIWSbk1cPLsJTKDTfa8',
        #'latlng' : latlng,
        'q' : latlng,
        'output' : 'json',
        'sensor' : sensor
    })

    url = REGEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    #print url
    result = json.load(urllib.urlopen(url))

    return json.dumps([s['address'] 
               for s in result['Placemark']])


def regeocode(latlng, sensor='false', **geo_args):
    """
        Reverse Geocoding
    """
    geo_args = ({
        'key' : 'AIzaSyBPqUNglpVE274TVIWSbk1cPLsJTKDTfa8',
        'latlng' : latlng,
        'sensor' : sensor
    })

    url = GEOCODE_BASE_URL + '?' + urllib.unquote(urllib.urlencode(geo_args))
    #print url
    result = json.load(urllib.urlopen(url))
    return json.dumps([s['formatted_address'] 
           for s in result['results']])


def regeocodeOSM(latlng, sensor='false', **geo_args):
    """
      OSM Reverse Geocoding
    """
    latlng = latlng.split(',')
    #lat = latlng[0]
    #lon = latlng[1]

    geo_args = ({
        'format' : 'json',
        'lat'  : latlng[0],
        'lon' : latlng[1],
        'zoom'  : 18,
        'addressdetails'  : 1,
        'email'  : 'jorge.toro@devmicrosystem.com'.encode("utf8")
    })

    url = OSM_REGEOCODE_BASE_URL + '?' + urllib.unquote(urllib.urlencode(geo_args))
    print url
    #result = json.load(urllib.urlopen(url))

    #return json.dumps([s['address'] 
    #                   for s in result['Placemark']])

