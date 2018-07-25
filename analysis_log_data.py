# PY script to extract data of interest. This is called from collect_log_data.sh
# Owner: Rohit Kumar, date: 07/24/2018

# This python script works only on local files. Ensure it is in the same directory as collect_log_data.sh
import os
import numpy as np
import sys
import csv
import pdb

if (len(sys.argv) < 3):
  print("ERROR: Invalid number of arguments to python script ")
  exit()

num_of_files = 1
_INPUT_FILE_ARR = [str(sys.argv[1])+'/second_data.txt']
_OUTPUT_FILE_ARR = [str(sys.argv[1])+'/second_out_data.txt']
_OUTPUT_CSV_ARR = [str(sys.argv[1])+'/second_out_data.csv']

first_match_phrase = "First_keyword"
second_match_phrase = "First_keyword_assoc"
third_match_phrase = "Second_keyword"
fourth_math_phrase = "Second_keyword_assoc"
fifth_match_phrase = "Third_keyword"
loc_match_phr = str(sys.argv[2]) # This is the string that has the path to the test results
log_index_phrase = "phrase_in_path_loc"
loc_end_phr = "file_name"
ignore_first_data = False
max_ids = 10
num_dig_in_id = 2
#pdb.set_trace()

# All IDs mapping
id_map_val = {}
id_map_val['10'] = 'one'
id_map_val['11'] = 'two'
id_map_val['12'] = 'three'
id_map_val['13'] = 'four'
id_map_val['14'] = 'five'
id_map_val['15'] = 'six'
id_map_val['16'] = 'seven'
id_map_val['17'] = 'eight'
id_map_val['20'] = 'nine'
id_map_val['21'] = 'ten'
id_map_val['22'] = 'eleven'
id_map_val['23'] = 'twelve'
id_map_val['24'] = 'thirteen'

#Process Cycles info fori CCH
for curr_file in range(0,num_of_files):
  with open(_OUTPUT_CSV_ARR[curr_file],'w') as csvfile:
    # Just open the CSV file once to Reset everything (prevent append from previous collection, if any)
    csv_row = ['First_data', 'Second_data', 'Third_data', 'Fourth_data']
    writer = csv.writer(csvfile)
    writer.writerow(csv_row)
  
  first_data_list = {}
  second_data_list = {}
  third_data_list = {}
  fourth_data_list = []
  fifth_data_list = []
  sixth_data_list = []
  valid_first_data_read = False
  valid_second_data_read = False
  first_data_stale = True
  out_file = open(_OUTPUT_FILE_ARR[curr_file], 'w');
  with open(_INPUT_FILE_ARR[curr_file],'rt') as in_file:
    for line in in_file:

      if second_match_phrase in line:
        start_index = line.index(second_match_phrase) + len(second_match_phrase)
        end_index = len(line) - 1;
        if line[start_index:end_index].isdigit() is True:
          if ignore_first_data is True:
            if first_data_stale is False:
              temp_pkt_val = int(line[start_index:])
              valid_first_data_read = True                    
          else:
            temp_pkt_val = int(line[start_index:])
            valid_first_data_read = True                    # Allow the second data type assoc to be read in next line
          

      if first_match_phrase in line:
        start_index = line.index(first_match_phrase) + len(first_match_phrase)
        end_index = len(line) - 1;
        if line[start_index:end_index].isdigit() is True:
          if ignore_first_data is True:
            if first_data_stale is True:
              first_data_stale = False    
            else:
              if valid_first_data_read is True:
                fourth_data_list.append(int(line[start_index:]))
                fifth_data_list.append(temp_pkt_val)
                valid_first_data_read = False           
          else:
            if valid_first_data_read is True:
              fourth_data_list.append(int(line[start_index:]))
              fifth_data_list.append(temp_pkt_val)
              valid_first_data_read = False           # Allow the second data type assoc to be read in next line
      
      ######################################### Next data type ########################################


      if fourth_math_phrase in line:
        start_index = line.index(fourth_math_phrase) + len(fourth_math_phrase)
        end_index = len(line) - 1;
        if line[start_index:end_index].isdigit() is True:
          temp_pkt_val = int(line[start_index:])
          valid_second_data_read = True                    
          

      if third_match_phrase in line:
        start_index = line.index(third_match_phrase) + len(third_match_phrase)
        id_index = line.index(fifth_match_phrase) + len(fifth_match_phrase)
        end_index = len(line) - 1;
        if line[start_index:end_index].isdigit() is True:
          if valid_second_data_read is True:
            if line[id_index:(id_index+num_dig_in_id)] in first_data_list:
              first_data_list[line[id_index:(id_index+num_dig_in_id)]].append(int(line[start_index:]))
              second_data_list[line[id_index:(id_index+num_dig_in_id)]].append(temp_pkt_val)
            else:
              first_data_list[line[id_index:(id_index+num_dig_in_id)]] = [int(line[start_index:])]
              second_data_list[line[id_index:(id_index+num_dig_in_id)]] = [temp_pkt_val]
            valid_second_data_read = False           
        else:
          valid_second_data_read = False           # reset it for the next pair 
            
      ######################################################################################

      if loc_match_phr in line:
        start_index = line.index(log_index_phrase) + len(log_index_phrase)
        end_index = line.index(loc_end_phr)
        out_file.write(line[start_index:end_index] + '\n')   
        if not fourth_data_list:
          out_file.write(" No valid information " + '\n')
          out_file.write('\n')
        else:  
          val_std_dev = round(np.std(fourth_data_list), 3)
          val_avg = round(np.mean(fourth_data_list), 3)
          val_max = np.amax(fourth_data_list)
          val_min = np.amin(fourth_data_list)
          
          sixth_data_list = np.true_divide(fourth_data_list, fifth_data_list)
          ratio_avg = np.round(np.mean(sixth_data_list), 3)
          ratio_sdev = round(np.std(sixth_data_list), 3)
          ratio_max = round(np.amax(sixth_data_list), 3)
          ratio_min = round(np.amin(sixth_data_list), 3)
          out_file.write(" Avg Val  = "+str(val_avg)+'\n')
          out_file.write(" Std Dev Val = "+str(val_std_dev)+'\n')
          out_file.write(" Max Val   = "+str(val_max)+'\n')
          out_file.write(" Min Val   = "+str(val_min)+'\n')
          out_file.write(" Avg ratio     = "+str(ratio_avg)+'\n')
          out_file.write(" Std Dev ratio = "+str(ratio_sdev)+'\n')
          out_file.write(" Max ratio     = "+str(ratio_max)+'\n')
          out_file.write(" Min ratio     = "+str(ratio_min)+'\n')
          out_file.write('\n')
          with open(_OUTPUT_CSV_ARR[curr_file],'a') as csvfile:
            writer = csv.writer(csvfile)
            csv_row = ['-', '-', '-', '-']
            csv_row[0] = str(line[start_index:end_index])
            csv_row[1] = str(val_avg)
            csv_row[2] = str(val_std_dev)
            csv_row[3] = str(ratio_avg)
            writer.writerow(csv_row)
          
        if bool(first_data_list) is False:
          out_file.write(" No valid next information " + '\n')
          out_file.write('\n')
        else:
          for key in sorted(first_data_list.iterkeys()):
            val_std_dev = round(np.std(first_data_list[key]), 3)
            val_avg = round(np.mean(first_data_list[key]), 3)
            val_max = np.amax(first_data_list[key])
            val_min = np.amin(first_data_list[key])
            out_file.write(" ID "+id_map_val[key]+" Avg val  = "+str(val_avg)+'\n')
            out_file.write(" ID "+id_map_val[key]+" Std Dev val = "+str(val_std_dev)+'\n')
            out_file.write(" ID "+id_map_val[key]+" Max val   = "+str(val_max)+'\n')
            out_file.write(" ID "+id_map_val[key]+" Min val   = "+str(val_min)+'\n')
            
            third_data_list[key] = np.true_divide(first_data_list[key], second_data_list[key])
            ratio_avg = np.round(np.mean(third_data_list[key]), 3)
            ratio_sdev = round(np.std(third_data_list[key]), 3)
            ratio_max = round(np.amax(third_data_list[key]), 3)
            ratio_min = round(np.amin(third_data_list[key]), 3)
            out_file.write(" ID "+id_map_val[key]+" Avg ratio     = "+str(ratio_avg)+'\n')
            out_file.write(" ID "+id_map_val[key]+" Std Dev ratio = "+str(ratio_sdev)+'\n')
            out_file.write(" ID "+id_map_val[key]+" Max ratio     = "+str(ratio_max)+'\n')
            out_file.write(" ID "+id_map_val[key]+" Min ratio     = "+str(ratio_min)+'\n')
            out_file.write('\n')
        
        fifth_data_list=[]
        fourth_data_list=[]
        sixth_data_list=[]
        second_data_list={}
        first_data_list={}
        third_data_list={}
        first_data_stale = True
        valid_first_data_read = False
        valid_second_data_read = False
  out_file.close()
  
