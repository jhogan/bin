#!/usr/bin/awk -f
{
    print $0; 
    if($2 == 0){
        ub+= $1;
    }else{
        t += $2;
        if($2 > $1) r += $2 - $1;
    }
    p += $1; 
} 

END {
    print "\nTotal: "  t "\nPaid: " p "\nRemaining: " r "\nUnbudgeted: " ub
}
