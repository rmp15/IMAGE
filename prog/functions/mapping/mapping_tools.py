import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cartopy as cp
from os import chdir
from pprint import pprint


def country_polygon(country_name):
    chdir('C:/Users/srh110/Documents/ne_10m_admin_0_countries')

    countries = cp.io.shapereader.Reader('ne_10m_admin_0_countries.shp')
    records = countries.records()
    geos = countries.geometries()

    geom_dict = {}
    for j in range(0, 255):
        record = next(records)
        cntry_name = record.attributes['NAME']

        country_polygon = record.geometry
        geom_dict[cntry_name] = country_polygon

    # aruba_geo = record.geometry
    # print(aruba_geo)
    # print(aruba_geo.type)
    #
    # p1 = Point( -70, 12.5)
    #
    # y = p1.within(aruba_geo)
    # print(y)
    try:
        polygon_borders = geom_dict[country_name]
        return polygon_borders
    except IndexError:
        return IndexError


def country_only_points(lats, lons, country_polygon):
    no_sites = np.size(lats)
    gcs = []
    for i in range(0, no_sites):
        p = Point(lons[i], lats[i])
        if p.within(country_polygon):
            gcs.append(i)
    return gcs

