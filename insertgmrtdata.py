import os
import glob

from config import *
from gmrtfileutils import GmrtFileUtility
from gmrtdbutils import GmrtDbUtils

class InsertGmrtDataController:
    """
    This Data controller does the following
    1 get the list of file exisiting in NCRANAS
    2 check the above files list alrady exisit in NAPSGOADB
    3 if files already exisit, check fot the path
    4 if all the above conditions gets satisfied, if the data is not in
        NAPSGOADB database, insert it
    """

    def checking_files_dbrecords(self):
        lta_file_list = GmrtFileUtility().get_lta_file_list()
        lta_db_list = GmrtDbUtils().get_database_lta_list()
        #print(len(lta_file_list), len(lta_db_list))
        print(lta_file_list, lta_db_list)
        #print(lta_file_list)
        #print(lta_db_list)


InsertGmrtDataController = InsertGmrtDataController()
InsertGmrtDataController.checking_files_dbrecords()
