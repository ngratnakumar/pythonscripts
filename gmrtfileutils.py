import os
import glob
from config import *

class GmrtFileUtility:
    
    def read_file(self):
        pass
    
    def get_lta_file_list(self):
        cycle_id = get_data('cycle_info','CYCLE_ID')
        cycle_path = get_data('data_storage','GMRTDATA5')+"CYCLE"+cycle_id+"/"
        lta_files = glob.glob(cycle_path+"*/*.lta*")
        lta_files.sort()
        return lta_files