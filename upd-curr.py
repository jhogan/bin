#! /usr/bin/python
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
import os
import sys
import re
if len(sys.argv) != 2:
    print ("Must supply directory to process")
    sys.exit(1)

CURRICDIR=sys.argv[1]


# regex for main xml file
# <multimediarefs ident="mm1" type="wmv">aropen.wmx</multimediarefs>
re_typeattr = re.compile('\stype\s*=\s*".*"')
re_mmref = re.compile(r'^.*<multimediarefs\s.*>(.*)</multimediarefs>.*$')

# regex for wmx
# <Ref href="aropen.avi"/>
re_href = re.compile(r'^.*<Ref\s.*href\s*=\s*"(.*)".*>.*$')


# recursivly examine each xml file in CURRICDIR
for dir, dirs, files in os.walk(CURRICDIR):
    for file in files:
        file = os.path.join(dir, file)
        changed = False
        out = ''
        if file[-4:] == '.xml':
            print "file:", file
            fh = open(file, 'r')
            for line in fh:
                m = re_mmref.match(line)
                if m: # is line a <multimediarefs> node
                    reffile = m.group(1) # get the wmx file
                    if (reffile[-4:] == '.wmx'): # did it turn out to be a wmx
                        reffile = os.path.join(dir, reffile)
                        print "\tencounterd:", line.rstrip()
                        if os.path.exists(reffile):
                            wmxh = open(reffile,'r')
                            for wmxline in wmxh:
                                m = re_href.match(wmxline)
                                if m: # is line a <Ref> node
                                    href = m.group(1)
                                    print "\twmx href:", href
                                    if href.find('../') != -1: # is the href a relative path
                                        tmpline = re_typeattr.sub(' type="flvstatehistory"', line)
                                        print '\t +type="flvstatehistory"'
                                    else:
                                        tmpline = re_typeattr.sub(' type="flv"', line)
                                        print '\t +type="FLV"'
                                    if line != tmpline:
                                        changed = True
                                        line = tmpline
                        else:
                            print "REFERENCE FILE MISSING:", reffile
                out += line
            if changed:
                fh.close()
                tmpfile = file + '.tmp'
                tmpfileh = open(tmpfile, 'w')
                print "\twriting:", tmpfile
                tmpfileh.write(out)
                tmpfileh.close()
                print "\tremove:", file
                os.remove (file)
                print "\trename:", tmpfile, "to", file
                os.rename (tmpfile, file)

                

