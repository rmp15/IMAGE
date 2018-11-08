import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon, LinearRing
import cartopy as cp
from os import chdir
from prog.functions.data.process_clag_stats_functions import *
import sys
from scipy.stats import rankdata
import scipy.io
from data.file_paths.file_paths import *


def country_polygon(country_name):

    countries = cp.io.shapereader.Reader(os.path.join(shapefile_europe, 'Europe.shp'))
    records = countries.records()
    geos = countries.geometries()

    geom_dict = {}
    for j in range(0, 255):
        record = next(records)
        cntry_name = record.attributes['NAME']

        # country_polygon = record.geometry
        country_polygon = next(geos)
        geom_dict[cntry_name] = country_polygon

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

