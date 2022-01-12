---
layout: post
title: Diebold FIT File Perl Script
date: '2010-07-28'
author: jtdub
tags:
- Diebold
- Perl Tips
- packetgeek.net
---

I wrote this to generate Diebold FIT files quickly. This script can generate a FIT file in a couple seconds in what would take me hours to do by hand.

```perl
#!/usr/bin/perl
#!C:\perl\bin\perl.exe

# May, 29, 2009
# Automatically creates a Diebold ATM FIT file
# based on a list of BIN numbers.

# 1) Takes each BIN number.
# 2) splits each BIN into two digit strings.
# 3) Assumes that each two digit string is a hex value.
# 4) Converts each hex value to decimal.
# 5) Makes sure each decimal number is three digits.
# 6) Creates the each incrementing FIT line.
# 7) Writes each FIT line to a specified file.

# If you are using a UNIX-Like OS, be sure to change
# the \\ in the $binPath, $fitPath, and $testPath
# so a single /

# User Definable Variables
# The directory in which the script looks for the input file
# and writes the output file(s).
$homeDir  = 'C:\Documents and Settings\williamsj\My Documents';
$binList  = "$ARGV[0]";
$fitList  = "$ARGV[1]";
$binPath = "$homeDir\\$binList";
$fitPath = "$homeDir\\$fitList";
# Do you want to add a FIT line so that the ATM can use
# a settlement card?
$settleCard = "1"; # 1 is On, 0 is Off
# Do you want to add a FIT line so that all other FI
# cards are defined? (Not "ON US")
$allOtherFI = "1"; # 1 is On, 0 is Off
# Having problems? Turning this on will create a file
# that has all corresponding outputs. It can be useful in
# troubleshooting the code.
# 1) BIN length
# 2) The BIN number
# 3) The hex values
# 4) The decimal values
$testData  = "0"; # 1 is On, 0 is Off
$testFile  = "testData.txt";
$testPath = "$homeDir\\$testFile";

# This is the meat of the script.
$num = "0";
if(!$ARGV[0]) {
 print "Error: You must specify a bin list.\n";
        print "$0 <input_bin_list> <output_fit_file>\n";
} elsif(!$ARGV[1]) {
 print "Error: You must specify a fit file to write to.\n";
        print "$0 <input_bin_list> <output_fit_file>\n";
} else {
if($settleCard eq 1) {
 open(FIT, ">$fitPath") or die "Can't open $fitPath.\n";
 print FIT "; Settlement card BIN (all 9's)\n";
 print FIT "000000153153153153153002000140000000000031000255000000000000000000000000000000000000000000000000000000000000000000000\c\\n";
 print FIT "; on-us BINs\n";
 close(FIT);
}
open(BINS, "$binPath") or die "Can't open $binPath.\n";
my @bins = ;
foreach $bins (@bins) {
 chomp($bins);
        $l = length($bins);
        @sbins = split(/(\d\d)/,$bins);
 if($l eq 10) {
         @b = ($sbins[1],$sbins[3],$sbins[5],$sbins[7],$sbins[9]);
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
                $dec[2] = hex($dec[2]);
                if(length($dec[2]) eq 2) {
                 $dec[2] = "0$dec[2]";
                } elsif(length($dec[2]) eq 1) {
                 $dec[2] = "00$dec[2]";
                }
                $dec[3] = hex($dec[3]);
                if(length($dec[3]) eq 2) {
                 $dec[3] = "0$dec[3]";
                } elsif(length($dec[3]) eq 1) {
                 $dec[3] = "00$dec[3]";
                }
                $dec[4] = hex($dec[4]);
                if(length($dec[4]) eq 2) {
                 $dec[4] = "0$dec[4]";
                } elsif(length($dec[4]) eq 1) {
                 $dec[4] = "00$dec[4]";
                }
 }
        if($l eq 9) {
         @b = ($sbins[1],$sbins[3],$sbins[5],$sbins[7],$sbins[8]);
                $b[4] = "$b[4]f";
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
                $dec[2] = hex($dec[2]);
                if(length($dec[2]) eq 2) {
                 $dec[2] = "0$dec[2]";
                } elsif(length($dec[2]) eq 1) {
                 $dec[2] = "00$dec[2]";
                }
                $dec[3] = hex($dec[3]);
                if(length($dec[3]) eq 2) {
                 $dec[3] = "0$dec[3]";
                } elsif(length($dec[3]) eq 1) {
                 $dec[3] = "00$dec[3]";
                }
                $dec[4] = hex($dec[4]);
                if(length($dec[4]) eq 2) {
                 $dec[4] = "0$dec[4]";
                } elsif(length($dec[4]) eq 1) {
                 $dec[4] = "00$dec[4]";
                }
        }
        if($l eq 8) {
         @b = ($sbins[1],$sbins[3],$sbins[5],$sbins[7]);
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
                $dec[2] = hex($dec[2]);
                if(length($dec[2]) eq 2) {
                 $dec[2] = "0$dec[2]";
                } elsif(length($dec[2]) eq 1) {
                 $dec[2] = "00$dec[2]";
                }
                $dec[3] = hex($dec[3]);
                if(length($dec[3]) eq 2) {
                 $dec[3] = "0$dec[3]";
                } elsif(length($dec[3]) eq 1) {
                 $dec[3] = "00$dec[3]";
                }
        }
        if($l eq 7) {
         @b = ($sbins[1],$sbins[3],$sbins[5],$sbins[6]);
                $b[3] = "$b[3]f";
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
                $dec[2] = hex($dec[2]);
                if(length($dec[2]) eq 2) {
                 $dec[2] = "0$dec[2]";
                } elsif(length($dec[2]) eq 1) {
                 $dec[2] = "00$dec[2]";
                }
                $dec[3] = hex($dec[3]);
                if(length($dec[3]) eq 2) {
                 $dec[3] = "0$dec[3]";
                } elsif(length($dec[2]) eq 1) {
                 $dec[2] = "00$dec[2]";
                }
        }
        if($l eq 6) {
         @b = ($sbins[1],$sbins[3],$sbins[5]);
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
                $dec[2] = hex($dec[2]);
                if(length($dec[2]) eq 2) {
                 $dec[2] = "0$dec[2]";
                } elsif(length($dec[2]) eq 1) {
                 $dec[2] = "00$dec[2]";
                }
        }
        if($l eq 5) {
         @b = ($sbins[1],$sbins[3],$sbins[4]);
                $b[2] = "$b[2]f";
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
                $dec[2] = hex($dec[2]);
                if(length($dec[2]) eq 2) {
                 $dec[2] = "0$dec[2]";
                } elsif(length($dec[2]) eq 1) {
                 $dec[2] = "00$dec[2]";
                }
        }
        if($l eq 4) {
         @b = ($sbins[1],$sbins[3]);
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
        }
        if($l eq 3) {
         @b = ($sbins[1],$sbins[2]);
                $b[1] = "$b[1]f";
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
                $dec[1] = hex($dec[1]);
                if(length($dec[1]) eq 2) {
                 $dec[1] = "0$dec[1]";
                } elsif(length($dec[1]) eq 1) {
                 $dec[1] = "00$dec[1]";
                }
        }
        if($l eq 2) {
         @b = ($sbins[1]);
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
        }
        if($l eq 1) {
         @b = ($sbins[0]);
                $b[0] = "$b[0]f";
                @dec = @b;
                $dec[0] = hex($dec[0]);
                if(length($dec[0]) eq 2) {
                 $dec[0] = "0$dec[0]";
                } elsif(length($dec[0]) eq 1) {
                 $dec[0] = "00$dec[0]";
                }
        }
        if($testData eq 1) {
         open(FILE, ">>$testPath")
                 or die "can't open file: $testFile.\n";
                print FILE "BIN Length: $l\n";
                print FILE "BINS: $bins\n";
                print FILE "HEX:  @b\n";
         print FILE "DEC:  @dec\n\n";
         close(FILE);
        }
        $d = "@dec";
        $d =~ s/ //g;
        $dl = length($d);
        if($dl eq 3) {
         $d = "$d 255255255255";
                $d =~ s/ //g;
        } if($dl eq 6) {
         $d = "$d 255255255";
                $d =~ s/ //g;
        } if($dl eq 9) {
         $d = "$d 255255";
                $d =~ s/ //g;
        } if($dl eq 12) {
         $d = "$d 255";
                $d =~ s/ //g;
        }
        open(FIT, ">>$fitPath") or die "Can't Open $fitPath.\n";
        foreach($d) {
         chomp($d);
                $num++;
                if($num <= "09") {
                 $fl = "00 $num 000 $d 001000140000000000031000255000000000000000000000000000000000000000000000000000000000000000000000";
                        $fl =~ s/ //g;
                        print FIT "$fl\c\\n";
                }
                if($num >= "10" && $num <= "99") {
                 $fl = "0 $num 000 $d 001000140000000000031000255000000000000000000000000000000000000000000000000000000000000000000000";
                        $fl =~ s/ //g;
                        print FIT "$fl\c\\n";
                }
                if($num >= "100" && $num <= "999") {
                 $fl = "$num 000 $d 001000140000000000031000255000000000000000000000000000000000000000000000000000000000000000000000";
                        $fl =~ s/ //g;
                        print FIT "$fl\c\\n";
                }
        }
        close(FIT);
}
if($allOtherFI eq 1) {
        $num++;
       open(FIT, ">>$fitPath") or die "Can't open $fitPath.\n";
        print FIT "; foreign BINs (All F's)\n";
        if($num <= "09") {
                $fl = "00 $num 000255255255255255000000140000000000031000255000000000000000000000000000000000000000000000000000000000000000000000";
                $fl =~ s/ //g;
                print FIT "$fl\c\\n";
        } elsif($num >= "10" && $num <= "99") {
               $fl = "0 $num 000255255255255255000000140000000000031000255000000000000000000000000000000000000000000000000000000000000000000000";
                $fl =~ s/ //g;
                print FIT "$fl\c\\n";
        } elsif($num >= "100" && $num <= "999") {
               $fl = "$num 000255255255255255000000140000000000031000255000000000000000000000000000000000000000000000000000000000000000000000";
                $fl =~ s/ //g;
                print FIT "$fl\c\\n";
        }
        close(FIT);
}
close(BINS);
}
```
