import unittest
import argparse
import pandas as pd
from save_to_panda import add_raw_traj, csv_to_panda

__author__ = 'jeromethai'

class TestDataImport(unittest.TestCase):

    def test_add_raw_traj(self):
        line1 = "23 [[[1.9, -2.4], '2014-09-02 11:10:15-07:00'], [[2.9, -5.4], '2014-09-02 11:14:27-07:00']]"
        line2 = "24 [[[33.9, -8.4], '2014-09-03 21:10:42-07:00'], [[32.9, -7.4], '2014-09-03 21:14:27-07:00'], [[31.4, -6.5], '2014-09-03 21:21:27-07:00']]"
        df = pd.concat([add_raw_traj(line1), add_raw_traj(line2)])
        print df
        self.assertTrue(len(df) == 5)
        self.assertTrue(len(df.loc['23']) == 2)
        self.assertTrue(len(df.loc['24']) == 3)
        self.assertTrue(df.loc['23'].loc[0]['lat'] == 1.9)
        self.assertTrue(df.loc['23'].loc[0]['lon'] == -2.4)
        self.assertTrue(df.loc['23'].loc[0]['timeStamp'] == '2014-09-02 11:10:15-07:00')
        self.assertTrue(df.loc['23'].loc[1]['lat'] == 2.9)
        self.assertTrue(df.loc['23'].loc[1]['lon'] == -5.4)
        self.assertTrue(df.loc['23'].loc[1]['timeStamp'] == '2014-09-02 11:14:27-07:00')
        self.assertTrue(df.loc['24'].loc[0]['lat'] == 33.9)
        self.assertTrue(df.loc['24'].loc[0]['lon'] == -8.4)
        self.assertTrue(df.loc['24'].loc[0]['timeStamp'] == '2014-09-03 21:10:42-07:00')
        self.assertTrue(df.loc['24'].loc[1]['lat'] == 32.9)
        self.assertTrue(df.loc['24'].loc[1]['lon'] == -7.4)
        self.assertTrue(df.loc['24'].loc[1]['timeStamp'] == '2014-09-03 21:14:27-07:00')
    
    
    def test_add_csv_to_panda(self):
        df = csv_to_panda('tests/sample_data.csv', add_raw_traj)
        self.assertTrue(len(df) == 5)
        self.assertTrue(len(df.loc['23']) == 2)
        self.assertTrue(len(df.loc['24']) == 3)
        self.assertTrue(df.loc['23'].loc[0]['lat'] == 1.9)
        self.assertTrue(df.loc['23'].loc[0]['lon'] == -2.4)
        self.assertTrue(df.loc['23'].loc[0]['timeStamp'] == '2014-09-02 11:10:15-07:00')
        self.assertTrue(df.loc['23'].loc[1]['lat'] == 2.9)
        self.assertTrue(df.loc['23'].loc[1]['lon'] == -5.4)
        self.assertTrue(df.loc['23'].loc[1]['timeStamp'] == '2014-09-02 11:14:27-07:00')
        self.assertTrue(df.loc['24'].loc[0]['lat'] == 33.9)
        self.assertTrue(df.loc['24'].loc[0]['lon'] == -8.4)
        self.assertTrue(df.loc['24'].loc[0]['timeStamp'] == '2014-09-03 21:10:42-07:00')
        self.assertTrue(df.loc['24'].loc[1]['lat'] == 32.9)
        self.assertTrue(df.loc['24'].loc[1]['lon'] == -7.4)
        self.assertTrue(df.loc['24'].loc[1]['timeStamp'] == '2014-09-03 21:14:27-07:00')
		

if __name__ == '__main__':
	unittest.main()