#!/bin/bash

if [ $# -eq 0 ] 
then
    echo ""
    echo "Usage $0 -p project name -o writable directory OR"
    echo ""
    echo "      $0 -n observation no -o writable directory "
    echo ""
    echo "Also You need  to have the directory named \"project\" or \"observation no\" in the current area"
    echo ""
    exit -1
fi

#XINFO=/usr/local/lute-2.00/xinfo  

#XINFO=/home/ratnakumar/insertScript-exp/lute-2.00/xinfo   

# Ratna Kumar: modified on 11012018 - Now accepts more than 4 digits 
# for XINFO upto 6 didits for observation no
XINFO=/root/scripts/insertDataScripts/lute-3.00/xinfo

#LTACLEAN=/usr/local/lute-2.00/ltaclean
LTACLEAN=/root/scripts/insertDataScripts/lute-3.00/bin/ltaclean

cleaninfo ()
{
      blank=" "
      echo "-------------------------------------------------------"

      for i in `echo $1 | sed s/,/\ /g`
      do
         if [ "$trueltafiles" ] 
         then
            trueltafiles=$trueltafiles,`readlink -f $i`
         else
            trueltafiles=`readlink -f $i`
         fi 
      done
      echo $trueltafiles  

      trueobslog=`readlink -f $4`

	IFS=',' read -ra ADDR <<< "$1"
	for i in "${ADDR[@]}"; do
	actname=`basename $i`
	actname=$actname".txt"
	echo " ************ "$actname" ******* "$ADDR"---**--"$i"-- trueobslo: "$trueobslog"--trueltafiles: "$trueltafiles	
      #echo $XINFOi" -l "$i" -o "$2-$actname" -n "$3" -f "$trueobslog" -p "$trueltafiles
      echo $XINFO " -l "$i" -o "$2-$actname" -n "$3" -f "$trueobslog" -p "$i
      $XINFO -l $i -o $2-$actname -n $3 -f $trueobslog -p $i
      if [ ${?} -ne 0 ] ; then
         echo "WARNING: XINFO FAILED -- TRYING TO CLEAN THE FILES"
         files=`echo $1 | awk -F, '{for(i=1;i<=NF;i++) printf ("%s ",$i)}'`
         #for fname in $files; do
        fname=$i  
	   echo CLEANING $fname
             bname=`basename $fname`
             $LTACLEAN -i $fname
             if [ "${?}" -ne "0" ]; then
                echo "ERROR: LTACLEAN FAILED ON $fname"
#                /bin/rm ltaclean_out.lta $bname
                exit 1
             fi
#             /bin/mv ltaclean_out.lta $bname
             if [ -n "$cname" ]; then
                 cname=$cname,$bname
                 ltafiles=$ltafiles$blank$bname
             else
                 cname=$bname
                 ltafiles=$bname
             fi
         #done
         echo "RUNNING $XINFO -l $cname -o $2-$actname -n $3 -f $4 2>> xinfo.errlog"
         $XINFO -l $cname -o $2-$actname -n $3 -f $4 -p $1
         if [ ${?} -ne 0 ] ; then
             echo "ERROR: XINFO FAILED on LTACLEANed files $cname"
         else
             echo "SUCCESS: XINFO WORKED ON THE LTACLEANed FILES"
             echo "$1" 
         fi
         echo DELETING SCRATCH FILES $ltafiles
#         /bin/rm $ltafiles
         echo ALL DONE
      fi
	done
}



traverse_proj() 
{
     arguments=""
     logfile="";
     obsno="";
     outputarea=$2
     
     if [ "$(ls -A $1)" ] 
     then
        echo "$1 dir exists, extracting the info..."
     else
        echo "Project $1, inside, is empty directory, exiting at travese_proj"
        exit -2
     fi

     for file in $1/*
     do

             echo "Found ${file}" | grep ".lta"
             if [[ $? -eq 0 ]] 
             then
                 arguments="$arguments$file,"
             fi

             echo "Found ${file}" | grep ".ltb"
             if [[ $? -eq 0 ]] 
             then
                 arguments="$arguments$file,"
             fi

             echo "Found ${file}" | grep "_gsb.lta"
             if [[ $? -eq 0 ]] 
             then
                 arguments="$arguments$file,"
             fi

             echo "Found ${file}" | grep ".obslog"
             if [[ $? -eq 0 ]] 
             then
                 logfile="$file"
                 obsno=$(basename "${file}" .obslog)
             fi
     done
          
         if [ ! "$arguments" ] 
         then
             echo "No lta files found, So exiting"
             exit -3
         fi

         if [ ! "$obsno" ] 
         then
             echo "No obslog found. So exiting"
             exit -4
         fi

           
         echo $arguments $outputarea/$obsno $obsno $logfile
         cleaninfo $arguments $outputarea/$obsno $obsno $logfile

         if [[ $? -eq 0 ]] ; then
         #echo "script created  $obsno.txt  for $obsno"
         echo "scripts created for $obsno"
         else
           echo "Xinfo failed for $obsno"
         fi

        # mv "$outputarea/$obsno".txt "$outputarea/$obsno".txt_old

}


traverse_obsno() 
{
    cd $1
    for i in *
    do
        traverse_proj $i $2
    done
    cd ..
}



outputarea=/tmp

while getopts ":p:n:o:" opt; do

   case $opt in
     o)
       outputarea=$OPTARG
       if [ ! -d $outputarea ]
       then
           echo "There is no such area"
           echo "Output will be written in /tmp"
           outputarea=/tmp
       fi
       ;;
     p)
       project=$OPTARG
       if [ -d $project ] 
       then
           if [ "$(ls -A $project)" ]
           then
                echo "Project $project dir exists, extracting the info..."
           else
                echo "$project is empty directory"
                exit -2
           fi
       else 
           echo "There is no $project directory in current working area" >&2
           exit -1
       fi
       ;;
     n)
       obsno=$OPTARG
       if [  -d $obsno ]
       then
           if [ "$(ls -A $obsno)" ]
           then
                echo "$obsno dir exists, extracting the info..."
           else
                echo "$obsno is empty directory"
                exit -2
           fi
       else
           echo "There is no $obsno directory in current working area" >&2
           exit -1
       fi
       ;;
     \?)
       echo "Invalid option: -$OPTARG" >&2
       exit 1
       ;;
     :)
       echo "Option -$OPTARG requires an argument." >&2
       exit 1
       ;;
   esac

done 

if [ -n "$project" ] 
then
    traverse_proj $project $outputarea
else
    if [ -n "$obsno" ]
    then
        traverse_obsno $obsno $outputarea
    fi
fi