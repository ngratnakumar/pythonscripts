from config import *
import os
import glob

class GmrtUtilites:
    def xinfo(self, file_path):
        xinfo_bin = get_data('gmrt_utils','XINFO')
        dirname = os.path.dirname(file_path)
        basename = os.path.dirname(file_path)
        obslog_file = glob.glob(dirname+'/*.obslog')[0]
        observation_no = 0
        if obslog_file:
            observation_no = os.path.basename(obslog_file).split('.')[0]
        return (observation_no, dirname, basename, obslog_file, file_path)
     
    def jxinfo(self):
        jxinfo_bin = get_data('gmrt_utils','XINFO')
        pass
    
    def ltaclean(self):
        ltaclean_bin = get_data('gmrt_utils','XINFO')
        pass
    
    def polarized_data(self):
        pass