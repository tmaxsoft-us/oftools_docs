#!/bin/bash

FILE_NAME=$1


if [ -f /opt/tmaxapp/OpenFrame/scripts/ASM_JSON/${FILE_NAME}.json ]; then
   cat /opt/tmaxapp/OpenFrame/scripts/ASM_JSON/${FILE_NAME}.json >>${FILE_NAME}.json
   exit 0
fi

echo "{" >>${FILE_NAME}.json
echo " \"entry_list\" : [" >>${FILE_NAME}.json
echo "   {" >>${FILE_NAME}.json
echo "     \"entry_name\" : \"${FILE_NAME}\"," >> ${FILE_NAME}.json
echo "     \"variable_parameter_list\" : {" >>${FILE_NAME}.json
echo "       \"max_length\" : 10" >>${FILE_NAME}.json
echo "     }" >>${FILE_NAME}.json
echo "   }">>${FILE_NAME}.json
echo " ],">>${FILE_NAME}.json
echo " \"program_name\" : \"${FILE_NAME}\",">>${FILE_NAME}.json
echo " \"version\" : 3" >>${FILE_NAME}.json
echo "}">>${FILE_NAME}.json
