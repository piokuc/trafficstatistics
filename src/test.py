import os
import traffic_stats
import unittest
import tempfile
import json

COLUMN_NAMES = """AADFYear,CP,Estimation_method,Estimation_method_detailed,Region,LocalAuthority,Road,RoadCategory,Easting,Northing,StartJunction,EndJunction,LinkLength_km,LinkLength_miles,PedalCycles,Motorcycles,CarsTaxis,BusesCoaches,LightGoodsVehicles,V2AxleRigidHGV,V3AxleRigidHGV,V4or5AxleRigidHGV,V3or4AxleArticHGV,V5AxleArticHGV,V6orMoreAxleArticHGV,AllHGVs,AllMotorVehicles""".split(',')

class TrafficTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, traffic_stats.app.config['DATABASE'] = tempfile.mkstemp()
        traffic_stats.app.config['TESTING'] = True
        self.app = traffic_stats.app.test_client()
        traffic_stats.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(traffic_stats.app.config['DATABASE'])

    def test_roads(self):
        rv = self.app.get('/traffic_stats/api/v1.0/roads/A3079')
        r = json.loads(rv.data)
        self.assertEqual(len(r), 16)

    def test_column_names(self):
        self.assertEqual(COLUMN_NAMES, traffic_stats.column_names())

    def test_find_road(self):
        self.assertEqual(len(traffic_stats.find_road('A3079')), 16)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
