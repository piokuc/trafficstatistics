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
        pass
        #self.db_fd, traffic_stats.app.config['DATABASE'] = tempfile.mkstemp()
        traffic_stats.app.config['TESTING'] = True
        self.app = traffic_stats.app.test_client()
        #traffic_stats.init_db()

    def tearDown(self):
        pass
        #os.close(self.db_fd)
        #os.unlink(traffic_stats.app.config['DATABASE'])

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

    def test_filter(self):
        params = {'StartJunction' : "A380/A383", 'EndJunction' : "Broadmeadow Lane, Teignmouth"}
        url = '/api/v1.0/filter?' + urllib.urlencode(params)
        print url
        rv = self.app.get(url)
        r = json.loads(rv.data)
        self.assertEqual(len(r), 16)

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
