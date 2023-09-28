


#!/usr/bin/perl
use strict;
use warnings;
use Term::ANSIColor qw(:constants);

my @listing = qx(ls -F);
foreach(@listing) {
  chomp $_;
  #print $_, "\n";
}

my @directories;
my @symlinks;
my @leftovers;

foreach my $object (@listing) {
  #if directory
  if($object =~ m/\/$/){
  push(@directories, $object)
  }
  #if symlink
  elsif($object =~ m/\@$/){
  push(@symlinks, $object)
  } else {
    push(@leftovers, $object)
    }
}

print GREEN "Directories and Symlinks\n", RESET;
foreach (@directories) {
        print BLUE $_, " ", RESET;
}
print "\n";
foreach (@symlinks) {
  print CYAN $_, " ", RESET;
}

print "\n------------------------\n";
print GREEN "Files\n", RESET;

foreach (@leftovers) {
  if($_ =~ m/\*$/) {
  print GREEN $_, " ", RESET;
  } else {
  print WHITE $_, " ", RESET;
  }
}
print "\n", RESET;
