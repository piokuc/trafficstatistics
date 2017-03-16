import shapefile
from shapely.geometry import shape, Point
import pyproj
import sqlite3

"""
This script populates table wards in the DATABASE, see WARDS_SCHEMA
It uses SHAPEFILE to find ward and district of each census point.
"""

DATABASE = '../data/Devon.sqlite'
WARDS_SCHEMA = """drop table if exists wards;
create table wards (CP Integer, Easting Integer, Northing Integer, ward Text, district Text);"""
SHAPEFILE = "../data/Wards_December_2016_Full_Clipped_Boundaries_in_Great_Britain.shp" 
BNG = pyproj.Proj(init='epsg:27700')
WGS84 = pyproj.Proj(init='epsg:4326')
DISTRICT = 'lad16cd'
WARD = 'wd16cd'

f = shapefile.Reader(SHAPEFILE) 
records = f.shapeRecords()
field_names = [field[0] for field in f.fields]

def point_to_ward_and_district(input_point):
    #p = pyproj.transform(BNG, WGS84, input_point[0], input_point[1])
    #point = Point(p[0], p[1])
    point = Point(pyproj.transform(BNG, WGS84, input_point[0], input_point[1]))
    for r in records:
        record_shape = shape(r.shape.__geo_interface__)
        if record_shape.contains(point):
            atr = dict(zip(field_names, r.record))
            return atr[WARD], atr[DISTRICT]
    return 'NOT FOUND', 'NOT FOUND'

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute('select distinct cp,easting,northing from traffic order by cp')
census_points = cur.fetchall()
conn.commit()
cur.executescript(WARDS_SCHEMA)
conn.commit()

for cp, easting, northing in census_points:
    ward, district = point_to_ward_and_district((easting, northing))
    row = (cp, easting, northing, ward, district)
    print ','.join(str(v) for v in row)
    cur.execute('insert into wards(cp,easting,northing,ward,district) values (?,?,?,?,?)', row)
    conn.commit()

conn.commit()
