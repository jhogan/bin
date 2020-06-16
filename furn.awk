#!/usr/bin/awk -f
{
    b = 15000;
    t += $2;
    print $0
} 

END {
    print "\n";
    r = b - t;
    print "Budget: \$"b "\nUsed: \$"t "\nRemaining: \$"r;
}
