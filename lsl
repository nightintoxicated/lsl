#!/usr/bin/perl
use strict;
use warnings;
use Term::ANSIColor qw(:constants);

my @listing = qx(ls -F);
foreach(@listing) {
  chomp $_;
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



print GREEN "Directories and Symlinks\n";
foreach (@directories) {
  print BRIGHT_BLUE $_, " ";
}
print "\n";
foreach (@symlinks) {
  print CYAN $_, " ";
}

print "\n\n";
print GREEN "Files\n";
foreach (@leftovers) {
  print WHITE $_, " ";
}
print "\n", RESET;
