from configparser import ConfigParser
import psycopg2

CONFIG_FILE = "gmrt.cfg"
DB_INFO = "gmrtdb.ini"

def dbconfig(filename=DB_INFO, section='pgdatabase'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_data(section, key):
    parser = ConfigParser()
    parser.read(CONFIG_FILE)
    return parser.get(section, key)

def select_from_db():
    """ Connect to the PostgreSQL database server """
    CYCLE_ID = get_data('cycle_info','CYCLE_ID')
    SQL1=" select  CONCAT(file_path,'/', coalesce(NULLIF(lta_file, ''), lta_gsb_file)) AS file_name from das.scangroup where file_path like '%CYCLE{}%';".format(CYCLE_ID)
    conn = None
    select_result = 0
    try:
        # read connection parameters
        params = dbconfig()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        cur.execute(SQL1)

        select_result = cur.fetchall()
        #print(select_result)
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return select_result
