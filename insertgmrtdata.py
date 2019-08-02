import os
import glob

from config import *
from gmrtfileutils import GmrtFileUtility
from gmrtdbutils import GmrtDbUtils
from gmrtutils import GmrtUtilites

class InsertGmrtDataController:
    """
    This Data controller does the following
    1 get the list of file exisiting in NCRANAS
    2 check the above files list alrady exisit in NAPSGOADB
    3 if files already exisit, check fot the path
    4 if all the above conditions gets satisfied, if the data is not in
        NAPSGOADB database, insert it
    """

    def check_for_backend_type(self, files_list):
        to_db_list = []
        gmrt_db_utils = GmrtDbUtils()
        files_list.sort(reverse = True)
        for each_lta in files_list:
            if ("TEST" not in each_lta or "test" not in each_lta or "TST" not in each_lta or "tst" not in each_lta):
                lta_file = os.path.basename(each_lta)
                proj_code = gmrt_db_utils.get_projcode_by_ltaname(lta_file)
                if GmrtDbUtils().get_projcode_by_ltaname(lta_file):
                    print("File already exisits in database ", lta_file)
                else:
                    print("Moving ... Forward")                    
                    if proj_code != 0:
                        to_db_list.append(each_lta)
                            
        if get_data('debug_mode','PRINTON'): 
            print("---------\n", to_db_list, "---------\n")
        return to_db_list
                                         
    def checking_files_dbrecords(self):
        lta_file_list = GmrtFileUtility().get_lta_file_list()
        # lta_db_list = GmrtDbUtils().get_database_lta_list()
        return lta_file_list    
        
    def generate_sqls(self, data_paths):
        if get_data('debug_mode','PRINTON'): 
            print("Inside generate_sqls", data_paths)
        sql_scripts = []
        for each_path in data_paths:
            sql_scripts.append(GmrtUtilites().xinfo(each_path))
        return sql_scripts
    
    def program_controller(self):
        gmrt_lta_files = self.checking_files_dbrecords()
        ltas_to_db = self.check_for_backend_type(gmrt_lta_files)
        sql_scripts = self.generate_sqls(ltas_to_db)
        if get_data('debug_mode','PRINTON'): 
            print(sql_scripts)
        

InsertGmrtDataController = InsertGmrtDataController()
InsertGmrtDataController.program_controller()