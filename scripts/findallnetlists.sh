#!/usr/intel/bin/bash
mv sch_list.txt sch_list.txt.bak
mv sch_list_sorted.txt sch_list_sorted.txt.bak
#find /p/hdk/archive/sdg74/noa/*/apr_noa/*/apr/outputs/ -name "*.apr_final.vg.gz" -exec stat -c "%n %y" {} \; | tee sch_list.txt
#find /p/hdk/archive/sdg74/noa/*/fev_rtl2net_noa/*/collateral/netlist/ -name "*.vg.gz" -exec stat -c "%n %y" {} \; | tee sch_list.txt
for subdir in /p/hdk/archive/sdg74/noa/*
do
   echo "***** parsing $subdir ****"
   find $subdir/fev_rtl2net_noa/*/collateral/netlist/ -name "*.vg.gz" -exec stat -c "%n %y" {} \; | tee -a sch_list.txt
done
echo "Sorting..."
awk -F/ '{print $NF " " $0 }' sch_list.txt | sort > sch_list_sorted.txt
echo "done"
#find /p/hdk/archive/sdg74/noa/*/caliber*/*/duet/ -name "*rser_report*" -exec stat -c "%n %y" {} \; | tee report_list.txt
# tom's line
# ls /p/hdk/archive/sdg74/noa/${line}/apr_noa/*/apr/outputs/${line}.*.vg.gz
