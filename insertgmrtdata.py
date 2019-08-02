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
        print("Inside chech_for_backend", files_list)
        to_db_list = []
        gmrt_db_utils = GmrtDbUtils()
        files_list.sort(reverse = True)
        print("^^^^^^^ reversed",files_list)
        for each_lta in files_list:
            if ("TEST" not in each_lta or "test" not in each_lta or "TST" not in each_lta or "tst" not in each_lta):
                print("This is a valid Observation", each_lta)
                lta_file = os.path.basename(each_lta)
                file_path = os.path.dirname(each_lta)
                proj_code = gmrt_db_utils.get_projcode_by_ltaname(lta_file)
                print("Something buchiki buchiki here --- ", proj_code)
                if '' not in proj_code:
                    print("Proper Project Code or proposal ID")
                    proj_code_with_date = os.path.basename(file_path)
                    if '_' in proj_code_with_date:
                        proj_code = proj_code_with_date[:6]
                    if ("DDT" in proj_code_with_date or "ddt" in proj_code_with_date):
                        proj_code = proj_code_with_date[:7].replace('DDT','ddt') 
                    backend_type = gmrt_db_utils.get_backend_type(proj_code)
                    print("Backend type exisits ?????")
                    if backend_type != 0:
                        print("Backend Exisit")
                        backend_type= backend_type[0]
                        print("+++++",each_lta, proj_code_with_date, proj_code, backend_type)
                        if ("GWB" in backend_type or "gwb" in backend_type):
                            if ("GWB" in each_lta or "gwb" in each_lta):
                                print(backend_type, "=== GWB")
                                to_db_list.append(each_lta)
                        if ("GSB" in backend_type or "gsb" in backend_type):
                            if (not "GWB" in each_lta or not "gwb" in each_lta):
                                print(backend_type, "*** GSB")
                                to_db_list.append(each_lta)
                            
        print("----------")
        print(to_db_list)
        print("----------")
        return to_db_list
                                         
    def checking_files_dbrecords(self):
        lta_file_list = GmrtFileUtility().get_lta_file_list()
        lta_db_list = GmrtDbUtils().get_database_lta_list()
        #print(len(lta_file_list), len(lta_db_list))
        # print(lta_file_list, lta_db_list)
        #print(lta_file_list)
        #print(lta_db_list)
        return lta_file_list, lta_db_list      
        
    def generate_sqls(self, data_paths):
        print("Inside generate_sqls", data_paths)
        sql_scripts = []
        for each_path in data_paths:
            sql_scripts.append(GmrtUtilites().xinfo(each_path))
        return sql_scripts
    
    def program_controller(self):
        gmrt_lta_files, gmrt_lta_db = self.checking_files_dbrecords()
        ltas_to_db = self.check_for_backend_type(gmrt_lta_files)
        sql_scripts = self.generate_sqls(ltas_to_db)
        print(sql_scripts)
        

InsertGmrtDataController = InsertGmrtDataController()
InsertGmrtDataController.program_controller()