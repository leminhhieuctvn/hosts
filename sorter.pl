use strict;
use warnings;
use File::Copy;

sub output {
    my( $lines, $fh ) = @_;
    return unless @$lines;
    print $fh shift @$lines; # print first line
    print $fh sort { lc $a cmp lc $b } @$lines;  # print rest
    return;
}

# Main processing loop (taking only one input file)
my $filename = shift @ARGV;
die "Usage: perl sorter.pl filtered_combined_blocklist.txt\n" unless defined $filename;

my $outFn = "hosts";

open my $fh, '<', $filename or die "open $filename: $!";
open my $fhOut, '>', $outFn or die "open $outFn: $!";
binmode($fhOut);
my $current = [];

while ( <$fh> ) {
    if ( m/^(?:[!\[]|[#|;]\s)/ ) {
        output $current, $fhOut;
        $current = [ $_ ];
    }
    else {
        push @$current, $_;
    }
}

output $current, $fhOut;
close $fhOut;
close $fh;
