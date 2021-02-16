#!/usr/intel/bin/perl

$listfilename = shift @ARGV;

open LISTFILE, $listfilename or die "cannot open list file $listfilename for read $!\n";
while(<LISTFILE>) {
    chomp;
    next if (/^#/);
    ($cellname, $block_count) = split /,/;
    $qismatfilename = "$cellname.vg.qismat.csv";
    print STDERR "opening $qismatfilename\n";
    $lines = 0;
    $total_cells = 0;
    open QISMATFILE, $qismatfilename or die "cannot open QISMAT file $qismatfilename for read: $!\n";
    while(<QISMATFILE>) {
        chomp;
        @line = split /,/;
        $cellname = $line[3];
        $cellcount = $line[4];
        $total_cells += $cellcount * $block_count;
        $lines += 1;
        $h{$cellname} += $cellcount * $block_count;
        print STDERR "   $cellname has $cellcount instances, total $total_cells\n";

    }
    close QISMATFILE;
    print STDERR "$lines lines, $total_cells cells\n";
}
close LISTFILE;

foreach $k (sort keys %h) {
    print "$k,$h{$k}\n";
}
