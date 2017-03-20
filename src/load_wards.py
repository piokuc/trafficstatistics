import shapefile
from shapely.geometry import shape, Point
import pyproj
import sqlite3
import db
from db import sql

"""
This script populates table wards in the DATABASE, see WARDS_SCHEMA
It uses SHAPEFILE to find ward and district of each census point.
"""

#DATABASE = '../data/Devon.sqlite'
WARDS_SCHEMA = """
drop table if exists wards;
create table wards (
    CP Integer, 
    Easting Integer, 
    Northing Integer, 
    ward Text, 
    district Text, 
    latitude Float, 
    longitude Float);"""
SHAPEFILE = "../data/Wards_December_2016_Full_Clipped_Boundaries_in_Great_Britain.shp" 
BNG = pyproj.Proj(init='epsg:27700')
WGS84 = pyproj.Proj(init='epsg:4326')
DISTRICT = 'lad16cd'
WARD = 'wd16cd'

f = shapefile.Reader(SHAPEFILE) 
records = f.shapeRecords()
field_names = [field[0] for field in f.fields]

def bng_to_wgs84(p):
    p = pyproj.transform(BNG, WGS84, p[0], p[1])
    return p

cache = {}
def wgs84_to_ward_and_district(p):
    try: return cache[(p[0],p[1])]
    except KeyError:
        for r in records:
            record_shape = shape(r.shape.__geo_interface__)
            if record_shape.contains(Point(p)):
                atr = dict(zip(field_names, r.record))
                cache[(p[0],p[1])] = (atr[WARD], atr[DISTRICT])
                return cache[(p[0],p[1])]
    return 'NOT FOUND', 'NOT FOUND'

census_points = sql('select distinct cp,easting,northing from traffic order by cp')

conn = sqlite3.connect(db.DATABASE)
cur = conn.cursor()
cur.executescript(WARDS_SCHEMA)
conn.commit()

for cp, easting, northing in census_points:
    lon_lat = bng_to_wgs84((easting, northing))
    ward, district = wgs84_to_ward_and_district(lon_lat)
    row = (cp, easting, northing, ward, district, lon_lat[1], lon_lat[0])
    print ','.join(str(v) for v in row)
    sql('insert into wards(cp,easting,northing,ward,district,latitude,longitude) values (?,?,?,?,?,?,?)', row)

conn.commit()
