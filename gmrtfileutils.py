import os
import glob
from config import *
import subprocess

class GmrtFileUtility:
    
    def get_lta_file_list(self):
        cycle_id = get_data('cycle_info','CYCLE_ID')
        cycle_path = get_data('data_storage','GMRTDATA5')+"/CYCLE"+cycle_id+"/"
        if get_data('debug_mode','PRINTON'): 
            print("CYCLE_PATH", cycle_path)
        lta_files = []
        for each_lta in glob.glob(cycle_path+"*/*.lta*")[:25]:
                lta_files.append(str(each_lta))
        lta_files.sort()
        if get_data('debug_mode','PRINTON'): 
            print("Inside get_lta_files_list", lta_files)
        return lta_files

    def run_shell_command(self, cmd): 
        cmd = cmd.split(' ')
        print(cmd)
        """
        stderr = ''
        stdout = ''
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
        except Exception as ex:
            print(ex, stderr, stdout)
        return (stderr, stdout)
        """