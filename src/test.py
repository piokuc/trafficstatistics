import os
import traffic_stats
import unittest
import tempfile
import json
import pprint
import urllib

pp = pprint.PrettyPrinter(indent=4)

class TrafficTestCase(unittest.TestCase):

    def setUp(self):
        traffic_stats.app.config['TESTING'] = True
        self.app = traffic_stats.app.test_client()

    def tearDown(self):
        pass

    def test_roads(self):
        rv = self.app.get('/api/v1.0/roads/A3079')
        r = json.loads(rv.data)
        self.assertEqual(len(r), 16)

    def test_wards(self):
        rv = self.app.get('/api/v1.0/wards/Appledore')
        r = json.loads(rv.data)
        self.assertEqual(len(r), 16)
        for e in r: self.assertEqual(e['ward'], 'Appledore')
        rv = self.app.get('/api/v1.0/wards/Yeo')
        r = json.loads(rv.data)
        self.assertEqual(len(r), 32)
        for e in r: self.assertEqual(e['ward'], 'Yeo')

    def test_filter(self):
        params = {'StartJunction' : "A380/A383",
                  'EndJunction' : "Broadmeadow Lane, Teignmouth",
                  'AADFYear' : '2015'}
        url = '/api/v1.0/filter?' + urllib.urlencode(params)
        rv = self.app.get(url)
        r = json.loads(rv.data)
        self.assertEqual(len(r), 1)
        for e in r:
            self.assertEqual(e['StartJunction'], "A380/A383")
            self.assertEqual(e['EndJunction'], "Broadmeadow Lane, Teignmouth")
            self.assertEqual(e['AADFYear'], 2015)

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

    def test_list_junctions(self):
        rv = self.app.get('/api/v1.0/list/junctions')
        r = json.loads(rv.data)
        self.assertEqual(len(r),263)
        self.assertTrue([u'Whiddon Drive', u'A361'] in r)

    def test_find_road(self):
        self.assertEqual(len(traffic_stats.find_road('A3079')), 16)

if __name__ == '__main__':
    unittest.main(verbosity=2)
