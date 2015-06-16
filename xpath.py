#! /usr/bin/python
# Accepts and xml file path and an xpath expresion 
# and returns the queried results
import libxml2, getopt, sys

def usage():
    print "Usage: %s file xpath" % sys.argv[0]
    sys.exit(1)

try:
    if len(sys.argv[1:]) != 2:
        usage()
    file, xpath = sys.argv[1:]
    doc = libxml2.parseFile(file)
    for val in doc.xpathEval(xpath):
        print val.content
    sys.exit(0)
    
except Exception , inst:
    print inst.args
    sys.exit(1)
