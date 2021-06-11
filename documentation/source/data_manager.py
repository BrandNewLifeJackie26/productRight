import pandas as pd
import sys


class DataManager:
    
    """
        DataManger Class to get data from different data source.
    """
    def __init__(self, data_path='') -> None:
        '''
        constructor method

        :param data_path: directory path of the data to load
        :type data_path: str
        :rtype: None
        '''
        self.data_path = data_path
        self.data = None

    # Fetch data
    # TODO: 1. can be converted to database; 2. specify nrows
    def fetch(self):
        '''
        Fetches data from data source
        
        :rtype: pandas Dataframe
        '''
        if not self.data:
            try:
                self.data = pd.read_csv(self.data_path, nrows=1000)
            except:  # TODO: more specific error handling
                print('Unexpected error:', sys.exc_info()[0])
        return self.data
