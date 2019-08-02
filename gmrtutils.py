from config import *
import os
import glob

class GmrtUtilites:
    
    def runxinfoalldb(self, file_path, obslog_file, observation_no, basename):
        outfile = str(observation_no)+"-"+basename+".json"
        runxinfo_bin = get_data('gmrt_utils','RUNXINFOALLDB')
        if get_data('debug_mode','PRINTON'): 
            print("RUNXINFOALLDB", file_path, obslog_file, observation_no, basename)
        return outfile
    
    def xinfo(self, file_path):
        if get_data('debug_mode','PRINTON'): 
            print("XINFO", file_path)
        xinfo_bin = get_data('gmrt_utils','XINFO')
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        obslog_file = glob.glob(dirname+'/*.obslog')[0]
        observation_no = 0
        if obslog_file:
            observation_no = os.path.basename(obslog_file).split('.')[0]
            return (
                self.jxinfo(
                    self.runxinfoalldb(
                        file_path, obslog_file, 
                        observation_no, basename
                    )
                )
            )
        else:
            return "No obslog.. Nothing can be done.."
     
    def jxinfo(self, outfile):
        jxinfo_bin = get_data('gmrt_utils','JXINFO')
        sql_file = outfile.replace('json','sql')
        if get_data('debug_mode','PRINTON'): 
            print("JXINO", sql_file)
        return sql_file
            
    
