#!/usr/bin/perl

use Getopt::Std;

$usage = '
    cell_counter_vg.pl infilename origname 

Parses an .vg format netlist to print the number of standard cells.  Note that this script
is set up for 10nm ec0 and e07 libraries.  The script would need to be modified for other
products.

Outputs these files:
  <infilename>.oneinst.csv  - contains the cell counts within one instance of each cell
  <infilename>.hashdump.csv - dump of the entire hierarchy for debuggging
  <infilename>.hier.csv     - a detailed print out of design info for every block of the design.
  <infilename>.qismat.csv   - to import into QISMAT

Parameters:
 -h : help - dump this message and die
 -d : print verbose debug information
 -v : specify SOFA voltage (default 0.8)
 -t : specify SOFA temperature (default 110)
 -a : specify SOFA altitude (default 0.9)
 -f : specify timing derating factor (default 0.5)

';

#### parse command line options #####

if ($#ARGV < 1) { die $usage }

getopts('hdv:t:a:');

if ($opt_h) { die $usage }

$v=0;
if ($opt_d) { $v = 1 };
if ( $v ) { print STDERR "verbose debug flag set\n"; }

if( $opt_v eq "") { $voltage = 0.8;     } else { $voltage = $opt_v; }
if( $opt_t eq "") { $temperature = 110; } else { $temperature = $opt_t; }
if( $opt_a eq "") { $altitude = 0.9;    } else { $altitude = $opt_a; }
if( $opt_f eq "") { $TDF = 0.5;         } else { $TDF = $opt_f; }

$infilename = shift @ARGV;
$topcell = shift @ARGV;

#####################################################################
# these functions need to be updated for libraries other than 10nm 
#####################################################################


#################################################################################
sub is_std_cell {
    $cell = shift @_;

    if ( ( substr($cell, 0, 3) eq "ec0") or ( substr($cell, 0,3) eq "e07") ) {
        return 1;
    } else {
        return 0;
    }

}

#################################################################################
sub rser_type {
    $rser_type = "UNKNOWN";
    $cell = shift @_;
    $rser_char = substr($cell,9,1);
    if( $rser_char eq "a" or $rser_char eq "b") {
        $rser_type = "STD";
    } elsif ( $rser_char eq "z" or $rser_char eq "w") {
        $rser_type = "SEUT";
    } elsif ( $rser_char eq "t" or $rser_char eq "y" or $rser_char eq "v") {
        $rser_type = "RCC";
    } elsif ( $rser_char eq "x" or $rser_char eq "u" or $rser_char eq "r") {
        $rser_type = "RTS";
    }
   return $rser_type

}

#################################################################################
sub celltype {
    $celltype = "UNKNOWN";
    $cell = shift @_;
   if( substr($cell, 3,1) eq "f" ) {
        $celltype = "FLOP";
    } elsif ( substr( $cell,3,1 ) eq "l" ) {
        $celltype = "LATCH";
    }
    return $celltype

}


#### print out the results ####

#################################################################################
sub print_oneinst {
    $outfilename = $infilename.".oneinst.csv";
    print STDERR "writing oneinst file $outfilename\n"; 
    open( my $fh, '>', $outfilename) or die "cannot open $outfilename for write: $!\n";
    print $fh "instance,level,module,cellname,count,stdcell,celltype,latchcount,flopcount,rser_type\n";
    while( my ($key, $value) = each( %ch ) ) {
        ($module, $cell) = split(/,/,$key);

        $flopcount=0;
        $latchcount=0;
        $celltype = &celltype( $cell ) ;
        
        if( $celltype eq "FLOP" ) {
            $flopcount = $value;
        } elsif ( $celltype eq "LATCH" ) {
            $latchcount = $value;
        }
        $stdcell = &is_std_cell($cell) ? "TRUE" : "FALSE";
        $rser_type = &rser_type( $cell );

        print $fh "oneinst,x,$key,$value,$stdcell,$celltype,$latchcount,$flopcount,$rser_type\n";
    }
    close $fh;
}


#### print out hierarchical

#################################################################################
sub dump_hier {
    $outfilename = $infilename.".hashdump.csv";
    print STDERR "writing hashdump file $outfilename\n";
    open( my $fh, '>', $outfilename) or die "cannot open $outfilename for write: $!\n";

    print $fh "mh_dump,module,cellname,count\n";
    foreach $module ( keys %mh ) {
        print $fh "module:$module\n";
        foreach $cell ( keys %{ $mh{$module} } ) {
            print $fh "mh_dump,x,$module,$cell,$mh{$module}{$cell}\n";
        }
    }
    close $fh;
}

#################################################################################
sub dump_flat {
    my $topcell = shift @_;
    my $path = shift @_;
    my $level = shift @_;
    my $fh = shift @_;

    foreach $instance ( keys %{ $ph{$topcell} } ) {
        $template = $ph{$topcell}{$instance};
        print STDERR "DEBUG:$topcell contains instance $instance of $template. Fullpath=$path/$instance \n" if $v;

        if ($template =~ /^ec0[fl]/) {
            print $fh "$path/$instance,$template,$level\n";
        }
        &dump_flat( $template, "$path/$instance", $level+1, $fh);
    }
}


#################################################################################
sub print_hier {
    my %lh = ();
    my %sh = ();

    my $topcell = shift @_;
    my $path = shift @_;
    my $level = shift @_;
    my $thiscellcount = shift @_;
    my $fh_hier = shift @_;
    my $fh_qismat = shift @_;


    if ($level > 15) {
        print STDERR "WARNING:  reached max recursion depth\n";
        return;
    }

    ### print out the QISMAT table, only if we're at the top level
    if($level == 0) {
        print STDERR "writing QISMAT data file\n";
        print $fh_qismat "Cluster,Block,FUB Name,Circuit Subtype,Instances,Design Style,Circuit Topology,Port Configuration,TDF,Logic TDF,Operating Voltage,Temperature,Altitude,Flop/Latch Protection\n";
        print $fh_hier   "Datatype,level,path,cellname,cellcount,stdcell,celltype,rser_type,thiscellcount\n";
    }

    #print STDERR "############################################################\n";
    #print STDERR "$path $topcell\n";
    foreach my $cell( keys %{ $mh{$topcell} } ) {
        #### count the cells at this level ####
        next if ( $cell eq "input" ) ;
        next if ( $cell eq "inout" ) ;
        next if ( $cell eq "output" ) ;
        next if ( $cell eq "wire" ) ;
        next if ( $cell eq "supply1" ) ;
        next if ( $cell eq "assign" ) ;
        my $cellcount = $mh{$topcell}{$cell};
        $celltype = &celltype( $cell );
        $stdcell = &is_std_cell($cell) ? "TRUE" : "FALSE";
        $rser_type = &rser_type($cell);
        print $fh_hier "thislevel,$level,$path,$cell,$cellcount,$stdcell,$celltype,$rser_type,$thiscellcount\n"; 
        $lh{$cell} += $cellcount * $thiscellcount;
        #print STDERR "$indent calling on $cell\n";

        %sh = &print_hier( $cell, "$path.$cell", $level+1, $cellcount, $fh_hier, $fh_qismat);
        foreach my $subhashcell( keys %sh ) {
             #print "$path adding subcell $subhashcell $sh{$subhashcell}\n";
             $lh{$subhashcell} += $sh{$subhashcell} * $thiscellcount;
        }
    }
    ### print out the summed up values
    foreach my $cell( keys %lh ) {
        $celltype = &celltype( $cell );
        $stdcell = &is_std_cell($cell) ? "TRUE" : "FALSE";
        $rser_type = &rser_type($cell);
        print $fh_hier "tobottom,$level,$path,$cell,$lh{$cell},$stdcell,$celltype,$rser_type\n";
    }

    ### print out the QISMAT table, only if we're at the top level
    if($level == 0) {
        $i=0;
        foreach my $cell( sort{ $lh{$b} <=> $lh{$a} } keys %lh ) {
            $celltype = &celltype( $cell );
            $stdcell = &is_std_cell($cell) ? "TRUE" : "FALSE";
            $rser_type = &rser_type($cell);
            if( ( $celltype ne "UNKNOWN" ) and ($rser_type ne "UNKNOWN") and $stdcell eq "TRUE") {
                print $fh_qismat "$path,$path,$path,$cell,$lh{$cell},$celltype,$rser_type,N/A,$TDF,1,$voltage,$temperature,$altitude,NONE\n";
                $i++;
            }
        }
        print STDERR "QISMAT file length:$i\n";
    }
    return %lh;
    
}

#################################################################################
# main
#################################################################################

#### initilize variables
%ch = (); # cell hash: key is "module,cell" the value is the count
%mh = (); # module hash: a hierarchical count of cells.  Has 2-level key: module and cell, and the value is the count.
%ph = (); # path hash: at each level has a key of module,instancename and the value is the template name


#### parse the input file ####

#################################################################################
print STDERR "parsing $infilename\n";
open INFILE, $infilename or die "cannot open $infilename for read: $!\n";
$inmodule=0;
$inmodulename=0;
$ininstance=0;
$modulename="none";
$l="";
while(<INFILE>) {
    chomp;
    s/^\s+//;  # strip off leading whitespace
    next if (/^\/\//);
    # print "LINE:$_\n";
    $l = $l.$_;
    if ($l=~/^endmodule/) {
        $inmodule=0;
        print STDERR "end of module $modulename in $_\n" if $v;
        $modulename="none";
        $l="";
        next;
    };
    if (/;/) { # the end of a line (or multi-line)
        print STDERR "\n###found end of line. im=$inmodule, in=$ininstance, imn=$inmodulename l=$l.\n" if $v;
        @line = split /\s+/, $l;
        if ( $#line < 1) {$l=""; next;}
        if ( $line[0] eq "") {$l=""; next;} # ignore blank lines
        if ( $l =~ /^\$ /) {$l=""; next;} # ignore comments
        if ( $l =~ /^\+/) {$l=""; next;} # ignore 2nd part of statements that are > 1 line
        if ( $l =~ /^\$\$\+/) {$l=""; next;} # ignore 2nd part of statements that are > 1 line
        if ( $line[0] eq "input" ) {$l=""; next;}
        if ( $line[0] eq "inout" ) {$l=""; next;}
        if ( $line[0] eq "output" ) {$l=""; next;}
        if ( $line[0] eq "wire" ) {$l=""; next;}
        if ( $line[0] eq "supply1" ) {$l=""; next;}
        if ( $line[0] eq "assign" ) {$l=""; next;}

        if ($l =~ /^module/) {
            $modulename=$line[1];
            $inmodule=1;
            print STDERR "found module $modulename in $_\n" if $v;
            $l="";
            next;
        }
        if( $ininstance == 0 and $inmodulename == 0 ) {
            if ($inmodulename) {
                $inmodulename=0;
                print STDERR "end of modulename : $l\n" if $v;
            } else {
                $ininstance = 0;
                $ch{ "$modulename,$line[0]" }++;
                $mh{ $modulename }{ $line[0] }++;
                $template = $line[0];
                $instance = $line[1];
                $ph{ $modulename }{ $instance } = $template;
                print STDERR "module $modulename has an instance of $template named $instance\n" if $v;
                #print STDERR "end of instance: $_\n";
            }
        }
        $l="";
    }
}
close INFILE;
print STDERR "done parsing \n";

#&print_oneinst();
#&dump_hier();

# because print_hier is recursive, we need to open the file out here:
$outfilename = $infilename.".flat";
print STDERR "writing flat file $outfilename\n";
open( my $fh, '>', $outfilename) or die "cannot open $outfilename for write: $!\n";

print $fh "path,template,level";
&dump_flat( $topcell, $topcell, 0, $fh ); 

close $fh;




