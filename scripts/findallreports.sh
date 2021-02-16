#!/usr/intel/bin/bash
#find /p/hdk/archive/sdg74/noa/*/caliber*/*/duet/ -name "*rser_report*" -exec stat -c "%n %y" {} \; | tee report_list.txt
mv report_list.txt report_list.txt.bak
for d in /p/hdk/archive/sdg74/noa/*/caliber*
do 
    find $d/*/duet/ -name "*rser_report*" -exec stat -c "%n %y" {} \; | tee -a report_list.txt
done

echo "Sorting..."
awk -F/ '{print $NF " " $0 }' report_list.txt | sort > report_list_sorted.txt
echo "done"
