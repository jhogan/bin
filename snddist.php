<?php
$t = 'string';
$t = shell_exec("echo $t | espeak -qx");
$f=null;
try{
    $f = fopen('/home/jhogan/var/cache/phonem', 'r');
    if(!$f) throw new Exception("Can't open file");

    while($l = fgets($f)){
        @list($ph, $w) = explode('  ', $l);
        $w = trim($w);
        $d = levenshtein($t, $ph);
        if($d < 7) echo "$ph - $w - $d\n";
    }
}
catch(Exception $ex){
    echo $ex;
}
finally{
    if($f) fclose($f);
}
