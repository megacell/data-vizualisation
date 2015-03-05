import unittest
import pandas as pd
from data_extract import extract_one_trajectory, extract_all_trajectories


__author__ = 'jeromethai'


class TestDataExtract(unittest.TestCase):
    
    def test_extract_one_trajectory(self):
    	df = pd.load('tests/sample_data.pkl')
    	print extract_one_trajectory(df, '24')
        #TO DO finish test


    def test_extract_all_trajectories(self):
        df = pd.load('tests/sample_data.pkl')
        #print df
    	print extract_all_trajectories(df) 
    	#TO DO finish test   	


if __name__ == '__main__':
	unittest.main()
        