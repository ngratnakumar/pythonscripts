from config import *
class GmrtDbUtils:

    def get_database_lta_list(self):
        lta_db_list = select_from_db()
        lta_list = []
        for each_lta_file in lta_db_list:
            lta_list.append(each_lta_file[0].strip())
        return lta_list

    def get_backend_type(self):
        pass
