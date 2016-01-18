<?php

$s = 'dacb';

$c = 2;

for($i=3; $i<=strlen($s); $i++) $c *= $i;

$s = str_split($s);

sort($s);

$j = 0;
for($i=0; $i<$c; $i++){
    echo(join($s) . "\n");
    if ($i % 2 == 0){
        list($x, $y, $z) = [2, 3, 1];
    }else{
        if($j++ % 2 == 0)
            list($x, $y, $z) = [3, 1, 1];
        else
            list($x, $y, $z) = [2, 1, 2];

    }

    array_splice($s, $y, 0, array_splice($s, $x, $z));
}
