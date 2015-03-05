import unittest
import argparse
import pandas as pd
from data_import import add_raw_traj, csv_to_panda, remove_static_points
import numpy as np
from utils import delta_time, distance_on_unit_sphere

__author__ = 'jeromethai'

class TestDataImport(unittest.TestCase):
    

    def assert_contents(self, df):
        self.assertTrue(len(df) == 5)
        self.assertTrue(len(df.loc['23']) == 2)
        self.assertTrue(len(df.loc['24']) == 3)
        val1 = 6373 * distance_on_unit_sphere(33.9, -8.4, 32.9, -7.4)
        val2 = delta_time('2014-09-03 21:10:42-07:00', '2014-09-03 21:14:27-07:00')

        self.assertTrue(df.loc['23'].loc[0]['lat'] == 1.9)
        self.assertTrue(df.loc['23'].loc[0]['lon'] == -2.4)
        self.assertTrue(df.loc['23'].loc[0]['timeStamp'] == '2014-09-02 11:10:15-07:00')
        self.assertTrue(df.loc['23'].loc[0]['dist_to_prev'] == 0.)
        self.assertTrue(df.loc['23'].loc[0]['time_to_prev'] == 0.)

        self.assertTrue(df.loc['23'].loc[1]['lat'] == 2.9)
        self.assertTrue(df.loc['23'].loc[1]['lon'] == -5.4)
        self.assertTrue(df.loc['23'].loc[1]['timeStamp'] == '2014-09-02 11:14:27-07:00')
        self.assertFalse(df.loc['23'].loc[1]['dist_to_prev'] == 0.)
        self.assertFalse(df.loc['23'].loc[1]['time_to_prev'] == 0.)

        self.assertTrue(df.loc['24'].loc[0]['lat'] == 33.9)
        self.assertTrue(df.loc['24'].loc[0]['lon'] == -8.4)
        self.assertTrue(df.loc['24'].loc[0]['timeStamp'] == '2014-09-03 21:10:42-07:00')
        self.assertTrue(df.loc['24'].loc[0]['dist_to_prev'] == 0.)
        self.assertTrue(df.loc['24'].loc[0]['time_to_prev'] == 0.)

        self.assertTrue(df.loc['24'].loc[1]['lat'] == 32.9)
        self.assertTrue(df.loc['24'].loc[1]['lon'] == -7.4)
        self.assertTrue(df.loc['24'].loc[1]['timeStamp'] == '2014-09-03 21:14:27-07:00')
        self.assertTrue(df.loc['24'].loc[1]['dist_to_prev'] == val1)
        self.assertTrue(df.loc['24'].loc[1]['time_to_prev'] == val2)


    def test_add_raw_traj(self):
        line1 = "23 [[[1.9, -2.4], '2014-09-02 11:10:15-07:00'], [[2.9, -5.4], '2014-09-02 11:14:27-07:00']]"
        line2 = "24 [[[33.9, -8.4], '2014-09-03 21:10:42-07:00'], [[32.9, -7.4], '2014-09-03 21:14:27-07:00'], [[31.4, -6.5], '2014-09-03 21:21:27-07:00']]"
        df = pd.concat([add_raw_traj(line1), add_raw_traj(line2)])
        self.assert_contents(df) 
    

    def test_add_csv_to_panda(self):
        df = csv_to_panda('tests/sample_data.csv', add_raw_traj)
        self.assert_contents(df)


    def test_remove_static_points(self):

        data = [[4.2, 0.0, 0.0], [6.4, 0.0, 100], [3.2, 0.0, 280], [7.8, 0.0, 2]]
        columns = ['data', 'dist_to_prev', 'time_to_prev']
        df = pd.DataFrame(data, index = range(4), columns = columns)
        df = remove_static_points(df, 300)
        self.assertTrue(len(df) == 2)
        self.assertTrue(df.loc[0]['data'] == 4.2)
        self.assertTrue(df.loc[1]['data'] == 7.8)
        self.assertTrue(df.loc[0]['dist_to_prev'] == 0.)
        self.assertTrue(df.loc[1]['dist_to_prev'] == 0.)
        self.assertTrue(df.loc[0]['time_to_prev'] == 0.)
        self.assertTrue(df.loc[1]['time_to_prev'] == 382)

        data = [[4.2, 0.0, 0.0], [6.4, 0.0, 350], [3.2, 1.0, 280], [7.8, 2.0, 2]]
        df = pd.DataFrame(data, index = range(4), columns = columns)
        df = remove_static_points(df, 300)
        self.assertTrue(len(df) == 4)

if __name__ == '__main__':
	unittest.main()
