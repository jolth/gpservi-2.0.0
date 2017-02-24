# -*- coding: utf-8 -*-
"""
    >>> import nominatim

### OpenStreeMap
    >>> a = nominatim.Openstreetmap('5.06889', '-75.51738',
    uri='http://nominatim.openstreetmap.org/reverse?', format='json')
    >>> a.decodeJSON()
    u'Gobernaci\xf3n de Caldas, Calle 22, Centro, Cumanday, Comuna Cumanday,
    Manizales, Centrosur, Caldas, 170001, Colombia'
    >>> 

or:
    >>> a = nominatim.Openstreetmap('5.06889', '-75.51738', format='json')
    >>> a.decodeJSON()
    u'Gobernaci\xf3n de Caldas, Calle 22, Centro, Cumanday, Comuna Cumanday,
    Manizales, Centrosur, Caldas, 170001, Colombia'

or:
    >>> a = nominatim.Openstreetmap('5.06889', '-75.51738')
    >>> a.decodeJSON()
    u'Gobernaci\xf3n de Caldas, Calle 22, Centro, Cumanday, Comuna Cumanday,
    Manizales, Centrosur, Caldas, 170001, Colombia'
"""
import urllib
import urllib2
import json
import re

class Reverse_Geocoding(object):
    def __init__(self, lat, lon, uri=None, **options):
        self.lat, self.lon = lat, lon
        self.options = options

        self.options.update(dict(lat=lat,lon=lon))
        
        if 'format' not in self.options: self.options.update({'format':'json'})
        query = urllib.urlencode(self.options)

        if re.search(self.options['format'],'(xml|XML)'):
            self.__data = self.getXML(query, uri)
        else:
            self.__data = self.getJSON(query, uri)

    def getJSON(self, query, uri=None):
        url = "%s%s" % (uri, query)
        return json.loads(urllib2.urlopen(url).read())

    def getXML(self):
        pass

    def decodeJSON(self):
        if 'display_name' in self.__data:
            return self.__data['display_name']
        return None

    def decodeXML(self):
        pass

class Openstreetmap(Reverse_Geocoding):
    def __init__(self, lat, lon, uri=None, **options):
        if uri is None:
            uri = 'http://nominatim.openstreetmap.org/reverse?'
            #uri = 'http://127.0.0.1:8181/nominatim/reverse.php?'

            Reverse_Geocoding.__init__(self, lat, lon, uri, **options)
        else:
            Reverse_Geocoding.__init__(self, lat, lon, uri, **options)
