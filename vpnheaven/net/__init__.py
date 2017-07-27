from collections import namedtuple
from geoip2.database import Reader
from enum import Enum
class Protocol(Enum):
    UDP = 1
    TCP = 2

class HostInfo:
    geo_reader = Reader("./geoip/GeoLite2-City.mmdb")
    asn_reader = Reader("./geoip/GeoLite2-ASN.mmdb")
    def __init__(self,ip):
        geo, asn = (self.geo_reader.city(ip), self.asn_reader.asn(ip))
        self.ip = ip
        self.continent = geo.continent.name
        self.country = geo.country.name
        self.country_code = geo.country.iso_code
        self.city = geo.city.name
        self.location = (geo.location.latitude, geo.location.longitude)
        self.timezone = geo.location.time_zone
        self.isp = asn.autonomous_system_organization

    def __str__(self):
        params = (self.ip, self.country, self.country_code, self.city, self.location[0], self.location[1], self.timezone, self.isp)
        return "Host(ip=%s, country=%s, country_code=%s, city=%s, location=(%f, %f), timezone=%s, isp=%s)" % params

    def __repr__(self):
        return self.__str__()
