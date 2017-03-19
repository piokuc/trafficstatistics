import os
from contextlib import closing

if os.getenv('EDITOR'):
    import sqlite3
    DATABASE = '/tmp/traffic.sqlite'

    def patch_prepared(s): return s
    def connect_db(): return sqlite3.connect(DATABASE)

    def init_db():
        try:
            with closing(connect_db()) as conn:
                with open('traffic.sql') as f:
                    script = f.read()
                    conn.cursor().executescript(script)
                conn.commit()
        except sqlite3.OperationalError as e:
            assert 'already exists' in e.message 
    init_db()

else:
    import psycopg2
    DATABASE = open('PG_CONNECTION').read()
    def patch_prepared(s): return s.replace('?','%s')
    def connect_db(): return psycopg2.connect(DATABASE)


def traffic_columns():
    return """AADFYear,CP,Estimation_method,Estimation_method_detailed,Region,LocalAuthority,Road,RoadCategory,Easting,Northing,StartJunction,EndJunction,LinkLength_km,LinkLength_miles,PedalCycles,Motorcycles,CarsTaxis,BusesCoaches,LightGoodsVehicles,V2AxleRigidHGV,V3AxleRigidHGV,V4or5AxleRigidHGV,V3or4AxleArticHGV,V5AxleArticHGV,V6orMoreAxleArticHGV,AllHGVs,AllMotorVehicles""".split(',')

def sql(*args):
    with closing(connect_db()) as conn:
        cur = conn.cursor()
        cur.execute(patch_prepared(args[0]), *args[1:])
        return cur.fetchall()
