import os
import glob
from config import *
import subprocess

class GmrtFileUtility:
    
    def read_file(self):
        pass

    def get_lta_file_list(self):
        cycle_id = get_data('cycle_info','CYCLE_ID')
        cycle_path = get_data('data_storage','GMRTDATA5')+"/CYCLE"+cycle_id+"/"
        #print(cycle_path)
        lta_files = []
        for each_lta in glob.glob(cycle_path+"*/*.lta*")[:1]:
                lta_files.append(str(each_lta))
        lta_files.sort()
	print("Inside get_lta_files_list", lta_files)
        return lta_files

    def run_shell_command(self, cmd): 
        cmd = cmd.split(' ')
        stderr = ''
        stdout = ''
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
        except Exception as ex:
            print(ex, stderr, stdout)
        return (stderr, stdout)
