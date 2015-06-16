s/\[dbo\]\.\[\([^]]\+\)\]/\1/
s/ default ((\(.*\)))/ DEFAULT (\1)/i 
/ Object: /d
s/use .*/use [[DB]]/i
s/with nocheck //i
/SET QUOTED_IDENTIFIER/d
/GRANT EXECUTE ON/d
/^\s*[Gg][Oo]\s*$/d

