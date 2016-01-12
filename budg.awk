#!/usr/bin/awk -f
{
    print $0; 
    if($3 == "") ub+= $1
    else         t += $2;
    p += $1; 
} 

END {
    print "\nTotal: "  t "\nPaid: " p "\nRemaining: " t-p "\nUnbudgeted: " ub
}
