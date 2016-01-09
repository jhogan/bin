#!/usr/bin/awk -f
{
    print $0; 
    if($3 == ""){
        ub+= $1
        p += $1
    }else{
        p += $1; 
        t += $2;
    }
} 

END {
    print "\nTotal: "  t "\nPaid: " p "\nRemaining: " t-p "\nUnbudgeted: " ub
}
