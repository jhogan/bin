<?php

$input = '6Zu';
try{

    $input = str_split($input);
    sort($input);

    $strmin = join(range(1, count($input)));
    $strmax = strrev($strmin);

    $intmin = intval($strmin);
    $intmax = intval($strmax);

    $num = $intmin;
    do{
        $strnum = strval($num);
        $chars = str_split($strnum);
        sort($chars);

        if(join($chars) == $strmin){
            foreach(str_split($strnum) as $c) echo $input[$c-1];
            echo "\n";
        }

    }while($num++ <= $intmax);
}catch(Exception $ex){
    print($ex);
}

