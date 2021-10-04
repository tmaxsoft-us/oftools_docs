#!/user/bin/python3
import sys
import subprocess
input_name=str(sys.argv[1])
output_name=str(sys.argv[2])
read_file = open(input_name, 'r')
write_file = open(output_name, 'w')

lines = read_file.readlines()
NEXT_LINE = False
VAR_FOR_NEXT = ""
ADD_LINKAGE = False
DATA_DIVISION = False
if subprocess.call("grep -E 'EIB-[A-Z]+' {}|grep -v '\*'".format(input_name), shell=True) == 0 or subprocess.call("grep -E 'EXEC\s*CICS' {}|grep -v '\*'".format(input_name), shell=True) == 0:
   if subprocess.call("grep ' LINKAGE SECTION.' {}".format(input_name), shell=True) != 0:
      ADD_LINKAGE = True



for each in lines:
  # if line is empty, continue
  if not each.strip():
     write_file.write(each)
  # if the line is commeted out, continue
  elif each[6] == "*" in each:
     write_file.write(each)
  # if line contains '=COPY', then commented out and modify to COPY
  elif "DATA DIVISION." in each and each[6] != "*":
     write_file.write(each)
     DATA_DIVISION = True
  elif "=COPY " in each:
     write_file.write("TMAXMD*" + each)
     temp=each.split()
     write_file.write("        COPY " + temp[temp.index("=COPY")+1] + ".\n")
  #if REPLACING exist, then continue
  elif " COPY " in each and " REPLACING " in each:
     write_file.write(each)
  # if COPY statement
  elif " COPY " in each:
     temp=each.split()
     # check there is '\' then continue
     if "\'" in each:
        write_file.write(each)
     # check there is 'IDMS' then continue
     elif " IDMS " in each:
        write_file.write(each)
     # check Copy does not have a period
     elif "." not in temp[temp.index("COPY")+1]:
        write_file.write("TMAXMD*" + each[7:])
        write_file.write("        COPY " + temp[temp.index("COPY")+1] + ".\n")
     # if a period existing, then continue
     elif "." in temp[temp.index("COPY")+1]:
        write_file.write(each)
  #if there is sequence sql statement
  elif "= NEXT VALUE FOR" in each or NEXT_LINE == True:
      temp = each.split()
      if temp[len(temp)-1] == "FOR":
         NEXT_LINE=True
         VAR_FOR_NEXT = temp
         write_file.write("TMAXMD*" + each[7:])
      elif NEXT_LINE == True:
         write_file.write("             SELECT " + temp[1] + ".NEXT "  + "\n")
         write_file.write("             INTO " + VAR_FOR_NEXT[2] + " FROM DUAL" + "\n")
         NEXT_LINE = False
         VAR_FOR_NEXT = ""
      else:
         write_file.write("TMAXMD*" + each[7:])
         write_file.write("             SELECT " + temp[7] + ".NEXT "  + "\n")
         write_file.write("             INTO " + temp[2] + " FROM DUAL" + "\n")
  #if there is "INSENSITIVE" statement with Declare or FETCH
  elif " INSENSITIVE " in each:
      if (" DECLARE " in each and " SCROLL " in each) or (" FETCH " in each):
         write_file.write("TMAXMD*" + each[7:72] + "\n")
         write_file.write(each[:72].replace("INSENSITIVE","") + "\n")
      else:
         write_file.write(each)
  #if EIB-USAGE
  elif " LINKAGE SECTION." in each and each[6] != "*" and DATA_DIVISION == True:
      if subprocess.call("grep -E 'EIB-[A-Z]+' {}".format(input_name), shell=True) == 0 or subprocess.call("grep -E 'EXEC\s*CICS' {}".format(input_name), shell=True) == 0:
         write_file.write(each)
         write_file.write("TMAXMD  COPY DFHEIBLK.\n")
      else:
         write_file.write(each)
         write_file.write("TMAXMD  COPY DFHEIBLK.\n")
  elif " PROCEDURE DIVISION." in each and each[6] != "*" and ADD_LINKAGE == True:
      write_file.write("TMAXMD  LINKAGE SECTION. \n")
      write_file.write("TMAXMD  COPY DFHEIBLK.\n")
      write_file.write(each)
      ADD_LINKAGE = False
  else:
     write_file.write(each)

read_file.close()
write_file.close()