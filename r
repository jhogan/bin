#! /bin/sh
TARGET="German Chancellor Angela Merkel has called US President Barack Obama
after receiving information that the US may have spied on her mobile phone.  A
spokesman for Mrs Merkel said the German leader views such practices... as
completely unacceptable.  Mrs Merkel called on US officials to clarify the
extent of their surveillance in Germany.  The White House said President Obama
had told Chancellor Merkel the US was not snooping on her communications.  The
United States is not monitoring and will not monitor the communications of the
chancellor, White House spokesman Jay Carney said on Wednesday.  The US has
been on the receiving end of anger from allies over spying allegations based on
material said to originate from fugitive American leaker Edward Snowden.
'Breach of trust' Continue reading the main story image of Nick Bryant Analysis"

tlen=${#TARGET}
count=0
clear
tput cup 2 10; echo -ne "$TARGET"
while [ "x$m" != "x$TARGET" ]; do
    r=`</dev/urandom tr -dc " ,.'A-Za-z0-9" | head -c$tlen`
    [ -z "$m" ] && m=$r
    mutated=0
    for i in `seq 0 $tlen`; do
        cr=${r:$i:1}; ct=${TARGET:$i:1}
        if [ "x$cr" = "x$ct" ]; then
            m0=$m; m=
            for j in `seq 0 $tlen`; do
               if [ $j -eq $i ]; then
                    m=${m}$cr
                    mutated=1
               else
                    m=${m}${m0:$j:1}
               fi
            done
        fi
    done
    c=$((c+1))
    if [ $mutated -eq 1 ]; then
        tput cup 5 10; 
        echo -ne "$m";
    fi
    #tput cup 9 10; echo -ne "$r"
done
echo
echo "Count: $c"

