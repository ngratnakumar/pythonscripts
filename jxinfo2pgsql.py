import argparse
import json
import sys
import os.path

def is_valid_file(parser, jsonfile):
        if not os.path.exists(jsonfile):
                parser.error("The file %s does not exist!" % jsonfile)
        else:
                return open(jsonfile, 'r').name


parser = argparse.ArgumentParser()

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-j',"--jsonfile", help="json filename to be processed", dest="jsonfile",required=True, metavar="<jsonfilename>", type=lambda x: is_valid_file(parser, x))
requiredNamed.add_argument('-o',"--outfile", help="output filename, this creates pgsql script file", required=True, metavar="<outputfilename>")

args = parser.parse_args()

def argumentParser():
	if format(args.jsonfile) == "None" or format(args.outfile) == "None":
		print("Syntax: argpar -f <jsonfile> -o <outputfile>")
	else:
		try:
			jsonParser(format(args.jsonfile), format(args.outfile))
		except Exception as ex:
			print(ex)
			pass

def jsonParser(jsonfile, outfile):
	f1 = open(jsonfile, 'r')
	f2 = open(jsonfile+".tmp", 'w')
	f3 = open(outfile, 'w')
	subarray = ['A','B','C','D']
	try:
		for line in f1:
			if '},]}' in line:
				f2.write(line.replace('},]}', '}]}'))
			else:
				f2.write(line)
		f1.close()
		f2.close()
		data=''
		with open(jsonfile+".tmp") as data_file:
			data = json.load(data_file)
			projectcode = data["observation_details"]["proj_code"]
			if 'DDT' in projectcode:
				projectcode = projectcode.replace('DDT','ddt')
		
			f3.write("CREATE OR REPLACE FUNCTION parseAndUpdate()  RETURNS void AS $$  DECLARE \n rowcount INTEGER;  \n myrecord RECORD;  \n skipscans BOOLEAN;  \n BEGIN \n ")

			f3.write("\nPERFORM * FROM das.observation where observation_no ="+data["observation_details"]["observation_no"]+" and proj_code='"+projectcode+"' ; \n GET DIAGNOSTICS rowcount = ROW_COUNT ; \n if(rowcount=0) then \n INSERT INTO das.observation(observation_no, proj_code)VALUES ("+data["observation_details"]["observation_no"]+", '"+projectcode+"');\nINSERT INTO das.log(observation_no, logfile )VALUES ("+data["observation_details"]["observation_no"]+", '"+data["observation_details"]["logfile"]+"');\n end if; \n")

			f3.write("\nskipscans := FALSE;\nPERFORM * FROM das.scangroup WHERE observation_no = "+data["observation_details"]["observation_no"]+" AND "+data["scangroup"]["dataFileColToBeUpdated_key"]+" = '"+data["scangroup"]["dataFileColToBeUpdated_val"]+"' AND file_path = '"+data["scangroup"]["file_path"]+"' ; \nGET DIAGNOSTICS rowcount = ROW_COUNT; \nif(rowcount <> 0) then \n   RAISE NOTICE '"+data["observation_details"]["observation_no"]+" - "+data["scangroup"]["file_path"]+"/"+data["scangroup"]["dataFileColToBeUpdated_val"]+" being skipped' ; \n   skipscans := TRUE;\nelse \n")

			f3.write("PERFORM lta_file, ltb_file, lta_gsb_file FROM das.scangroup where observation_no = "+data["observation_details"]["observation_no"]+" and ("+data["scangroup"]["col1_key"]+"='"+data["scangroup"]["col1_val"]+"' or "+data["scangroup"]["col2_key"]+"='"+data["scangroup"]["col2_val"]+"') and file_path='"+data["scangroup"]["file_path"]+"'; \n GET DIAGNOSTICS rowcount = ROW_COUNT ; \n if(rowcount=0) then \n INSERT INTO das.scangroup(observation_no,"+data["scangroup"]["dataFileColToBeUpdated_key"]+",  "+data["scangroup"]["col1_key"]+", "+data["scangroup"]["col2_key"]+", corr_version, sta_time, num_pols, num_chans, lta_time, file_path , "+data["scangroup"]["fileSize_key"]+") VALUES ("+data["observation_details"]["observation_no"]+",  '"+data["scangroup"]["dataFileColToBeUpdated_val"]+"' , '', '', '"+data["scangroup"]["corr_version"]+"',  "+data["scangroup"]["sta_time"]+", "+data["scangroup"]["num_pols"]+", "+data["scangroup"]["num_chans"]+", "+data["scangroup"]["lta_time"]+" , '"+data["scangroup"]["file_path"]+"' , "+data["scangroup"]["fileSize_val"]+");  \n else \n UPDATE das.scangroup set "+data["scangroup"]["dataFileColToBeUpdated_key"]+"='"+data["scangroup"]["dataFileColToBeUpdated_val"]+"', "+data["scangroup"]["fileSize_key"]+"="+data["scangroup"]["fileSize_val"]+" where observation_no ="+data["observation_details"]["observation_no"]+" and ("+data["scangroup"]["col1_key"]+"='"+data["scangroup"]["col1_val"]+"' or "+data["scangroup"]["col2_key"]+"='"+data["scangroup"]["col2_val"]+"') and file_path='"+data["scangroup"]["file_path"]+"'; \n end if; \n \nend if;\n\n\n\nIF (skipscans = false) then \n")

			for scandata in data['scans']:
				#f3.write("INSERT INTO das.scans( observation_no, scangroup_id, scan_no, proj_code, source, ra_2000, dec_2000, date_obs, ant_mask, band_mask, calcode, qual, ra_date, dec_date, dra, ddec, sky_freq1, sky_freq2, rest_freq1, rest_freq2, lsr_vel1, lsr_vel2, chan_width, net_sign1, net_sign2, net_sign3, net_sign4, onsrc_time,source_position)VALUES ( "+data["observation_details"]["observation_no"]+", (select scangroup_id from das.scangroup where "+data["scangroup"]["dataFileColToBeUpdated_key"]+"='"+data["scangroup"]["dataFileColToBeUpdated_val"]+"' and observation_no="+data["observation_details"]["observation_no"]+" and file_path='"+data["scangroup"]["file_path"]+"'), "+scandata["scan_no"]+", '"+data["observation_details"]["proj_code"]+"', TRIM('"+scandata["source"]+"'), "+str(scandata["ra_2000"])+", "+str(scandata["dec_2000"])+", '"+scandata["date_obs"]+"', "+scandata["ant_mask"]+", "+scandata["band_mask"]+", "+scandata["calcode"]+","+scandata["qual"]+", "+scandata["ra_date"]+", "+scandata["dec_date"]+", "+scandata["dra"]+", "+scandata["ddec"]+", "+scandata["sky_freq1"]+", "+scandata["sky_freq2"]+", "+scandata["rest_freq1"]+", "+scandata["rest_freq2"]+", "+scandata["lsr_vel1"]+", "+scandata["lsr_vel2"]+", "+scandata["chan_width"]+", "+scandata["net_sign1"]+", "+scandata["net_sign2"]+", "+scandata["net_sign3"]+", "+scandata["net_sign4"]+", "+scandata["onsrc_time"]+","+scandata["source_position"]+"); \n")
				f3.write("INSERT INTO das.scans( observation_no, scangroup_id, scan_no, proj_code, source, ra_2000, dec_2000, date_obs, ant_mask, band_mask, calcode, qual, ra_date, dec_date, dra, ddec, sky_freq1, sky_freq2, rest_freq1, rest_freq2, lsr_vel1, lsr_vel2, chan_width, net_sign1, net_sign2, net_sign3, net_sign4, onsrc_time,source_position)VALUES ( "+data["observation_details"]["observation_no"]+", (select scangroup_id from das.scangroup where "+data["scangroup"]["dataFileColToBeUpdated_key"]+"='"+data["scangroup"]["dataFileColToBeUpdated_val"]+"' and observation_no="+data["observation_details"]["observation_no"]+" and file_path='"+data["scangroup"]["file_path"]+"'), "+scandata["scan_no"]+", '"+projectcode+"', TRIM('"+scandata["source"]+"'), "+str(scandata["ra_2000"])+", "+str(scandata["dec_2000"])+", '"+scandata["date_obs"]+"', "+scandata["ant_mask"]+", "+scandata["band_mask"]+", "+scandata["calcode"]+","+scandata["qual"]+", "+scandata["ra_date"]+", "+scandata["dec_date"]+", "+scandata["dra"]+", "+scandata["ddec"]+", "+scandata["sky_freq1"]+", "+scandata["sky_freq2"]+", "+scandata["rest_freq1"]+", "+scandata["rest_freq2"]+", "+scandata["lsr_vel1"]+", "+scandata["lsr_vel2"]+", "+scandata["chan_width"]+", "+scandata["net_sign1"]+", "+scandata["net_sign2"]+", "+scandata["net_sign3"]+", "+scandata["net_sign4"]+", "+scandata["onsrc_time"]+","+scandata["source_position"]+"); \n")

			f3.write("\nEND IF;\nEND; \n $$ LANGUAGE PLPGSQL; \n select parseAndUpdate();")
			f3.close()

			print("SQL Script Created")
	except Exception as ex:
		print(ex)
	else:
		print("Parsing done, file generated -- "+args.outfile)

argumentParser()

