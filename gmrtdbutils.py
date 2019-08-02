from config import *
class GmrtDbUtils:

    def get_database_lta_list(self):
        CYCLE_ID = get_data('cycle_info','CYCLE_ID')
        SQL1=" select CONCAT(file_path,'/', coalesce(NULLIF(lta_file, ''), lta_gsb_file)) AS file_name from das.scangroup where file_path like '%CYCLE{}%';".format(CYCLE_ID)
        lta_db_list = select_from_db(SQL1)
        lta_list = []
        for each_lta_file in lta_db_list:
            lta_list.append(each_lta_file[0].strip())
        lta_list.sort(reverse = True)
        return lta_list

    def get_backend_type(self, proj_code):
        if get_data('debug_mode','PRINTON'): print(proj_code)
        sql = "select backend_type from gmrt.proposal where proposal_id = '{}'".format(proj_code)
        backend_type = select_from_db(sql)
        if get_data('debug_mode','PRINTON'): print(backend_type,"-- getting from db")
        if backend_type:
            return backend_type
        else:
            return 0


    def get_projcode_by_ltaname(self, lta_file):
        sql = " select distinct proj_code from das.scangroup sg inner join das.scans s on s.scangroup_id = sg.scangroup_id where lta_gsb_file = '{}' or lta_file = '{}'".format(lta_file, lta_file)
        proj_code = select_from_db(sql)
        if proj_code:
            return proj_code
        else:
            return 0