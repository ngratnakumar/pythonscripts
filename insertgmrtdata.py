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
        for each_lta in files_list:
            lta_file = os.path.basename(each_lta)
            file_path = os.path.dirname(each_lta)
            proj_code = GmrtDbUtils.get_projcode_by_ltaname(lta_file)
            if not proj_code:
                proj_code_with_date = os.path.basename(file_path)
                if '_' in proj_code_with_date:
                    proj_code = proj_code_with_date[:6]
                else:
                    proj_code = proj_code_with_date[:7] 
                backend_type = GmrtDbUtils.get_backend_type(proj_code)
                if "GWB" in backend_type OR "gwb" in backend_type:
                    if "GWB" in each_lta OR "gwb" in each_lta:
                        to_db_list.append(each_lta)
                else:
                    if not "GWB" in each_lta OR not "gwb" in each_lta:
                        to_db_list.append(each_lta)
        return to_db_list
                        

    def check_db_file_path(self, dblist):
        ltas_to_db = []
        for each_lta in dblist:
            each_lta = each_lta.replace('//','/')
        pass
                    
    def checking_files_dbrecords(self):
        lta_file_list = GmrtFileUtility().get_lta_file_list()
        lta_db_list = GmrtDbUtils().get_database_lta_list()
        #print(len(lta_file_list), len(lta_db_list))
        print(lta_file_list, lta_db_list)
        #print(lta_file_list)
        #print(lta_db_list)
        return lta_file_list, lta_db_list      
        
    def program_controller(self):
        gmrt_lta_files, gmrt_lta_db = self.checking_files_dbrecords()
        ltas_to_db = self.check_for_backend_type(gmrt_lta_files)
        

InsertGmrtDataController = InsertGmrtDataController()
InsertGmrtDataController.checking_files_dbrecords()
