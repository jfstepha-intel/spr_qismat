#!/usr/intel/bin/perl

# The blocks info file is pulled with:
# blocks_info.pl -csv ',' -headers template,name,physical_parent,type,release,chops -sortby template > spr_blocks_info_19ww06.txt
# (was blocks_info.pl -headers template,name,physical_parent -fval type=part -sortby template > spr_blocks_info_19ww04.csv)
# from within the SPR design evironment

$infilename = shift @ARGV;
$schlistfilename = shift @ARGV;
$outpath = '/nfs/sc/disks/sdg74_3328/PycharmProjects/spr_qismat/stats_20ww24_in_progress/reports';

print STDERR "parsing blocks_info file...\n";

open INFILE, $infilename or die "cannot open $infilename for read: $!\n";
while(<INFILE>) {
    chomp;
    ($template, $name, $physical_parent, $type, $release, $chops) = split /,/;
    # print STDERR "got $template, $name, $physical_parent, $type, $release, $chops\n";
    $rec = {};
    $rec->{'template'} = $template;
    $rec->{'name'} = $name;
    $rec->{'physical_parent'} = $physical_parent;
    $rec->{'type'} = $type;
    $rec->{'release'} = $release;
    $rec->{'chops'} = $chops;
    push @blocklist, $rec;
}
close INFILE;

print STDERR "parsing report list file...\n";
open INFILE, $schlistfilename or die "cannot open $infilename for read:$!\n";
$prev_fname = "";
while(<INFILE>) {
    ($fname, $fdate, $ftime, $ftzone, $fpath) = split /\s+/;
    #print STDERR "got $fname, $fdate, $ftime, $ftzone, $fpath\n";
    $rec = {};
    $rec->{'name'} = $fname;
    $rec->{'date'} = $fdate;
    $rec->{'time'} = $ftime;
    $rec->{'path'} = $fpath;
    if($prev_fname ne $fname) {
        print STDERR "pushing $prevrec->{'name'}\n";
        push @schlist, $prevrec;
    }
    $prevrec = $rec;
    $prev_fname = $fname;
}

close INFILE;


#print STDERR "dump of schlist:\n";
#for $href( @schlist) {
#    print STDERR "{ ";
#    for $role ( keys %$href ) {
#        print STDERR "$role=$href->{$role} ";
#    }
#    print STDERR "}\n";
#}

print STDERR "pulling files...\n";
for $href( @blocklist ){
    print STDERR "*** $href->{'template'} **** \n";
    ## find in schlist
    $found=0;
    for $schref( @schlist ) {
       $n = $schref->{'name'};
       #if( $schref->{'name'} eq $href->{'template'}.".syn_final.vg.gz" ) {
#       print STDERR "comparing $schref->{'name'} to".$href->{'template'}."_rser_report.txt.gz\n";
       if( $schref->{'name'} eq $href->{'template'}."_rser_report.txt.gz" ) {
           $found=1;
           print STDERR "  found at $schref->{'path'}\n";
           $href->{'path'} = $schref->{'path'};
           $href->{'date'} = $schref->{'date'};
           $href->{'time'} = $schref->{'time'};
           print STDERR "  copying $schref->{'path'} to $outpath\n";
           print STDERR "  status=".`cp $schref->{'path'} $outpath`."\n";
       }
    }
    if( $found==0 ){
        print STDERR "  NOT FOUND\n";
        $href->{'path'} = 'NOT FOUND';
        $href->{'date'} = 'NOT FOUND';
        $href->{'time'} = 'NOT FOUND';
    }
}
print STDERR "writing final status list...\n";

#  header
print "name,template,physical_parent,type,release,chops,date,time,path\n";

for $href( @blocklist ) {
    print "$href->{'name'},$href->{'template'},$href->{'physical_parent'},$href->{'type'},$href->{'release'},$href->{'chops'},$href->{'date'},$href->{'time'},$href->{'path'}\n";
}

print STDERR "DONE\n";
