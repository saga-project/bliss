#!/usr/bin/perl -w

BEGIN { 
  use strict; 
  use File::Find;
  use File::Copy;

  sub fix_markup;
}

find ( {'wanted' => \&fix_markup, 'no_chdir' => 1}, ".");

sub fix_markup
{
  my $file  = $File::Find::name;
  my $text  = "";

  return if -d $file;
  return if $file !~ /\.py$/i;
# return if $file !~ /^.\/test\.py$/i;

# print "$file\n";

  my $in_list = 0;

  open    (IN, "<$file") or die "Cannot open  <$file: $!\n";
  foreach my $line ( <IN> ) 
  {
    if ( ! $in_list && $line =~ /^\s*[\-\*]\s+/o )
    {
      $text    .= "\n";
      $text    .= $line;
      $in_list  = 1;
    }
    elsif ( $in_list && $line !~ /^\s*[\-\*]\s+/o )
    {
    # $text    .= "\n";
      $text    .= $line;
      $in_list  = 0;
    }
    else
    {
      $text    .= $line;
    }
  }
  close   (IN);

  $text =~ s/U{(.*?)}/`$1`_/sg;
  $text =~ s/L{([-_\.a-zA-Z0-9 ]*?\(.*?\))}/:func:`$1`/sg;
  $text =~ s/L{([-_\.a-zA-Z0-9 ]*?)}\s*\(/:func:`$1` \(/sg;
  $text =~ s/L{(.*?)}/:class:`bliss.saga.$1`/sg;
  $text =~ s/B{(.*?)}/**$1**/sg;
  $text =~ s/\@param /:param /sg;
  $text =~ s/\@type /:type /sg;

  move ("$file","$file.bak") or die "Cannot open <>$file: $!\n";

  open  (OUT, ">$file") or die "Cannot open  >$file: $!\n";
  print  OUT  $text;
  close (OUT);
}

