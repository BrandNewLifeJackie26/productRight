import pandas as pd
import sys


"""
    DataManger: get data from different data source
"""


class DataManager:
    def __init__(self, data_path='') -> None:
        self.data_path = data_path
        self.data = None

    # Fetch data
    # TODO: 1. can be converted to database; 2. specify nrows
    def fetch(self):
        if not self.data:
            try:
                self.data = pd.read_csv(self.data_path, nrows=1000000)
            except:  # TODO: more specific error handling
                print('Unexpected error:', sys.exc_info()[0])
        return self.data
