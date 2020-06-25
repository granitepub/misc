#!/usr/bin/awk -f 
# ----------------------------------------------------------------------
# Author: Roger Delgado
# Date: November 2018
# Purpose:
#   Use AWK to search for roll numbers that contain a prefix and a size
# Variables:
#   This script takes in 2 variables:
#       roll and size
# Example Usage:
# ./findrolls.awk -v roll="<prefix>" -v size=<integer> file (*.csv)
#
# This script only works on csv files created for the .xlsx templates used to create the reports.
# ----------------------------------------------------------------------

BEGIN { 
    FS=",";
    OFS="---";
}


{
    if (match($3, /^[A-Z][A-Z0-9]{6,}/))
        print $3, $6
    if (match($4, /^[A-Z][A-Z0-9]{6,}/))
        print $4, $7
}



#{
    #if ($3 ~ /^[A-Z][A-Z0-9]{8,}/)
        #print $3, $6
    #if ($4 ~ /^[A-Z][A-Z0-9]{8,}/)
        #print $4, $7
#}

# Uncomment this code and comment the code above
# to search for specific rolls based on prefix
# See notes at the top of the file.
# -----------------------------------------------
#{
    #if ($4 ~ roll && $7 <= size)  
        #{ print $4, $7 }
    #if ($3 ~ roll && $6 <= size)  
        #{ print $3, $6 }

#}

END {
    #print "---------------------"
    #print  "Search Complete!!!"
    }
