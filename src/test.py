import os
import traffic_stats
import unittest
import tempfile
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

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
        rv = self.app.get('/api/v1.0/roads/A3079')
        r = json.loads(rv.data)
        self.assertEqual(len(r), 16)

    def test_wards(self):
        rv = self.app.get('/api/v1.0/wards/Appledore')
        r = json.loads(rv.data)
        self.assertEqual(len(r), 16)
        rv = self.app.get('/api/v1.0/wards/Yeo')
        r = json.loads(rv.data)
        self.assertEqual(len(r), 32)
        #pp.pprint ([(v['AADFYear'],v['CP']) for v in r])

    def test_list_wards(self):
        rv = self.app.get('/api/v1.0/list/wards')
        r = json.loads(rv.data)
        self.assertEqual(len(r),120)
        self.assertTrue(u'Loddiswell & Aveton Gifford' in r)

    def test_list_roads(self):
        rv = self.app.get('/api/v1.0/list/roads')
        r = json.loads(rv.data)
        self.assertEqual(len(r),34)
        self.assertTrue(u'M5' in r)

    def test_column_names(self):
        self.assertEqual(COLUMN_NAMES, traffic_stats.column_names())

    def test_find_road(self):
        self.assertEqual(len(traffic_stats.find_road('A3079')), 16)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
