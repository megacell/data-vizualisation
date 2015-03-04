import unittest
from utils import distance_on_unit_sphere, delta_time, TOL

__author__ = 'jeromethai'

class TestUtils(unittest.TestCase):
    
    def test_distance_on_unit_sphere(self):
    	#location of Eiffet tower
    	lat1, lon1 = 48.858557, 2.294481
    	#location of Statue of Liberty
    	lat2, lon2 = 40.689473, -74.044468
    	dist = distance_on_unit_sphere(lat1, lon1, lat2, lon2)
    	# check against http://www.johndcook.com/lat_long_distance.html
    	self.assertTrue(abs(dist*3960 - 3628) <= 1.) # in miles
    	self.assertTrue(abs(dist*6373 - 5839) <= 1.) # in km
    	# same locations
    	self.assertTrue(distance_on_unit_sphere(lat1, lon1, lat1+TOL/2, lon1+TOL/2) == 0.0)


    def test_delta_time(self):
    	start = "2014-09-02 23:56:11-07:00"
    	end = "2014-09-02 23:56:11-07:00"
    	self.assertTrue(delta_time(start, end) == 0.0)
    	start = "2014-09-02 11:55:11-07:00"
    	end = "2014-09-02 11:56:12-07:00"
    	self.assertTrue(delta_time(start, end) == 61.0)
    	start = "2014-09-02 11:55:11-07:00"
    	end = "2014-09-02 14:56:12-07:00"
    	self.assertTrue(delta_time(start, end) == 3*3600+61.0)
    	start = "2014-09-02 23:56:12-07:00"
    	end = "2014-09-02 23:55:11-07:00"
    	self.assertTrue(delta_time(start, end) == -61.0)
    	try:
    	    start = "2014-09-02 23:56:12-07:00"
    	    end = "2014-09-03 23:55:11-07:00"
    	    self.assertTrue(delta_time(start, end) == -61.0)
    	    self.assertTrue(False)
    	except AssertionError:
    		self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()