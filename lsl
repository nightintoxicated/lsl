#!/usr/bin/perl
$| = 1;
use strict;
use warnings;
use Term::ANSIColor qw(:constants);

my @listing;
if (exists $ARGV[1]) {
  print "Warning, recommended one folder at a time\nor use regular ls for readability\n";
  sleep 2;
}

if (!exists $ARGV[0]) {
  @listing = qx(ls -F);
} else {
  @listing = qx(ls -F @ARGV);
}



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

my $length = 0;
my $longest = 0;
foreach (@directories) {
  if (defined $length) {
    $length = length($_);
    if($length > $longest) {
      $longest = $length;
}}}

# Time to print stuff 
my $counter = 0;
print GREEN "Directories and Symlinks\n", RESET;

foreach my $dir_item (@directories) {
  if($counter eq 4) {
    #for columns
    print "\n";
    $counter = 0;
  }
  print BLUE $dir_item, "  ", RESET;

  my $a = length($dir_item);
  my $spaces = $longest - $a;
  my $i = 0;
  while ($i < $spaces) {
    print " ";

    $i +=1;
  }
$counter += 1;
}

#print symlinks
print "\n";
$counter = 0;
foreach my $sym_item (@symlinks) {
  if($counter eq 4) {
    print "\n";
    $counter = 0;
  }
  print CYAN $sym_item, "  ", RESET;

  my $a = length($sym_item);
  my $spaces = $longest - $a;
  my $i = 0;
  while ($i < $spaces) {
    print " ";
    $i +=1;
  }
$counter += 1;
}


print "\n------------------------\n";
print GREEN "Files\n\n", RESET;


$counter = 0;
$longest = 0;

foreach (@leftovers) {
  if (defined $length) {
    $length = length($_);
    if($length > $longest) {
      $longest = $length;
}}}


foreach my $file_item (@leftovers) {
  if($counter eq 4) {
    print "\n";
    $counter = 0;
  }
  if($file_item =~ m/\*$/) {
  #green for files with a * (executables) 
  print GREEN $file_item, "  ", RESET;
  } else {
  print WHITE $file_item, "  ", RESET;
  }

  my $a = length($file_item);
  my $spaces = $longest - $a;
  my $i = 0;
  while ($i < $spaces) {
	  print " ";
  $i +=1;
 }
$counter += 1;
}
print "\n", RESET;

