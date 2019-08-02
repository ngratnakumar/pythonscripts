from config import *
import os
import glob

class GmrtUtilites:
    
    def runxinfoalldb(self, file_path, obslog_file, observation_no, basename):
        outfile = str(observation_no)+"-"+basename
        print("Inside runxinfodb", file_path, obslog_file, observation_no, basename)
        return(file_path, obslog_file, observation_no, outfile)
    
    def xinfo(self, file_path):
        print("Inside Xinfo", file_path)
        xinfo_bin = get_data('gmrt_utils','XINFO')
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        obslog_file = glob.glob(dirname+'/*.obslog')[0]
        observation_no = 0
        print(file_path, obslog_file, observation_no, basename)
        if obslog_file:
            observation_no = os.path.basename(obslog_file).split('.')[0]
            return self.runxinfoalldb(file_path, obslog_file, observation_no, basename)
        else:
            return "No obslog.. Nothing can be done.."
     
    def jxinfo(self, file_path):
        jxinfo_bin = get_data('gmrt_utils','XINFO')
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        sql_file = file_path+'.sql'
        return (jxinfo_bin, dirname, basename, sql_file)
            
    
