from config import *
class GmrtDbUtils:

    def get_database_lta_list(self):
        CYCLE_ID = get_data('cycle_info','CYCLE_ID')
        SQL1=" select CONCAT(file_path,'/', coalesce(NULLIF(lta_file, ''), lta_gsb_file)) AS file_name from das.scangroup where file_path like '%CYCLE{}%';".format(CYCLE_ID)
        lta_db_list = select_from_db(SQL1)
        lta_list = []
        for each_lta_file in lta_db_list:
            lta_list.append(each_lta_file[0].strip())
        return lta_list

    def get_backend_type(self):
        pass


    def get_projcode_by_ltaname(self, lta_file):
        sql = "select proj_code from das.scangroup where lta_gsb_file = '{}' or lta_file = '{}'".format(lta_file)
        proj_code = select_from_db(sql)
        print(proj_code)