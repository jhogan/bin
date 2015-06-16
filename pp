#!/bin/bash
pp_fgred='31'
pp_fggreen='32'
pp_fgyellow='33'
pp_fgblue='34'
pp_fgmagenta='35'
pp_fgcyan='36'
pp_fgwhite='37'
pp_fgdefault='38' # seems to work

pp_bgblack='40'
pp_bgred='41'
pp_bggreen='42'
pp_bgyellow='43'
pp_bgblue='44'
pp_bgmagenta='45'
pp_bgcyan='46'
pp_bgwhite='47'
pp_bgdefault='48' # seems to work

pp_nostyle=0
pp_bold=1
pp_underscore=4
pp_blink=5
pp_inverse=7
pp_concealed=8

function pp_cursor_invisible(){
    tput civis
}
function pp_cursor_visible(){
    tput cnorm
}
function pp_clear(){
    echo -e -n "\E[2J"
}
function pp_echoline(){
    pp_echo "$@"
    echo
}
function pp_clearline(){
    echo -en "\033[K"
}
function pp_echo(){
    msg=$1
    shift
    for style in $@; do
         [ $style -ge 0 -a $style -le 10 ] && deco=$style
         [ $style -ge 30 -a $style -le 39 ] && fg=$style
         [ $style -ge 40 -a $style -le 49 ] && bg=$style
    done
    [ -z "$deco" ] && deco=pp_nostyle
    
    esc="\E[$deco;"
    [ -n "$fg" ] && esc="$esc;$fg"
    [ -n "$bg" ] && esc="$esc;$bg"
    esc="${esc}m"
    
    pp_clearline

    echo -ne "${esc}"
    echo -n "$msg"
}

function pp_settop(){
    echo -e "\033[0;0H"
}

pp_clear
pp_cursor_invisible
pp_settop
pp_echo "date:" "$pp_nostyle" "$pp_bgblack" "$pp_fggreen"
pp_echo " `date`" "$pp_bgwhite" "$pp_fgdefault"
sleep 1
pp_echoline
pp_echo "date:" "$pp_nostyle" "$pp_bgblack" "$pp_fggreen"
pp_echo " `date`" "$pp_bgwhite" "$pp_fgdefault"
pp_cursor_visible
