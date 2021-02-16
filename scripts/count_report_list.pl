#!/bin/bash
mkdir -p /tmp/jfstepha
while read p; do
    echo "## Processing $p"
    #b=$(basename $p _rser_report.txt)
    #b=$(basename $p .apr_final.vg)
    b=$(basename $p .vg)
    echo "## (base name=$b)"
    g=${b%.gz}
    echo "## (g = $g)"
    bb=${g%.vg}
    echo "## (bb = $bb)"
    echo "## copying $p to /tmp/jfstepha/$b"
    cp fev/$b /tmp/jfstepha/$b
    echo "## gunzipping"
    gunzip /tmp/jfstepha/$b
    echo "## running perl script"
    #echo "command: cell_counter_vg.pl $p $b > $p.csv"
    #cell_counter_vg.pl $p $b > $p.csv
    echo "command: cell_counter_vg.pl $g $bb "
    ../scripts/cell_counter_vg.pl /tmp/jfstepha/$g $bb

done <$1
