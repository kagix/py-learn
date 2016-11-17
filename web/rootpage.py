from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from bs4 import BeautifulSoup
from xml.dom.minidom import parse, parseString
import sys

def getVersionFromFile(textlines):
    theVersion = 0
    if theVersion == 0:
        for text in textlines:
#            print text
            if "17.10.2016" in text:
                theVersion=20161017
                break

    if theVersion == 0:
        for text in textlines:
#            print text
            if "01.04.2016" in text:
                theVersion=20160401
                break

    return theVersion


def parseAttrs(attrs):
    info=""
    info2=""
    ival = 0
    for attr in attrs:
        pair=attr.split(":")
        if pair[0] ==  "left":
            info = info + "@left:"+pair[1];
            ival = int(pair[1].strip("px"))
            ival = ival + 19
            info2 = info2 + "@left:"+ str(ival);
        if pair[0] ==  "top":
            info = info + "@top:"+pair[1];
            info2 = info2 + "@top:"+pair[1];
        if pair[0] ==  "width":
            info = info + "@width:"+pair[1];
            info2 = info2 + "@width:"+pair[1];
        if pair[0] ==  "height":
            info = info + "@height:"+pair[1];
            info2 = info2 + "@height:"+pair[1];
#   print "INFO=" + info
#   print "INFO2=" + info2
    return (info,info2)


def tokanita(value):
    l = len(value)
    ret = []
    tok = ""
    if (l%2) == 0:
        lst = list(value)
        for c in lst:
            if tok == "":
                tok = tok + c
            else:
                tok = tok + c
                ret.append(tok)
                tok = ""
    return ret    
    

def processOneSpan(spans,info,info2,file):
    #print "nbspans = 1"
    value = spans[0].firstChild.nodeValue
    if value:
        if  " " in value:
            print "DECALARE\n"
            values = value.split(" ")
            if len(values) == 2:
                linfo = info + "@" + values[0]
                print( linfo + "\n")
                file.write( linfo + "\n")
                tokens = tokanita(values[1])
                for tok in tokens:
                    linfo = info2 + "@" + tok
                    print( linfo + "\n")
                    file.write( linfo + "\n")
            
        else:
            tokens = tokanita(value)
            for tok in tokens:
                linfo = info2 + "@" + tok
                print( linfo + "\n")
                file.write( linfo + "\n")

def processFirstSpan(spans,info,info2,file):
    span1 = spans[0]

    value = spans[0].firstChild.nodeValue
    if value:
        if  " " in value:
            print "DECALARE\n"
            values = value.split(" ")
            if len(values) == 2:
                linfo = info + "@" + values[0]
                print( linfo + "\n")
                file.write( linfo + "\n")
                tokens = tokanita(values[1])
                for tok in tokens:
                    linfo = info2 + "@" + tok
                    print( linfo + "\n")
                    file.write( linfo + "\n")
            
        else:
            tokens = tokanita(value)
            for tok in tokens:
                linfo = info2 + "@" + tok
                print( linfo + "\n")
                file.write( linfo + "\n")

    value = spans[1].firstChild.nodeValue
    if value:
        if  " " in value:
            print "DECALARE\n"
            values = value.split(" ")
            if len(values) == 2:
                linfo = info + "@" + values[0]
                print( linfo + "\n")
                file.write( linfo + "\n")
                tokens = tokanita(values[1])
                for tok in tokens:
                    linfo = info2 + "@" + tok
                    print( linfo + "\n")
                    file.write( linfo + "\n")
            
        else:
            tokens = tokanita(value)
            for tok in tokens:
                linfo = info2 + "@" + tok
                print( linfo + "\n")
                file.write( linfo + "\n")




#print "\n".join(sys.argv)
f = open(sys.argv[1], 'r')
lines2 = f.readlines()
f.close();
f = open(sys.argv[1], 'r')
lines = f.read()
f.close();
#print sys.argv[1]
#print sys.argv[1].split("/");
outname = "output/" + sys.argv[1].split('/')[1] + ".txt"
print outname
#parser.feed(lines);

version=getVersionFromFile(lines2)
print str(version)

soup = BeautifulSoup(lines)
soup2 = None
mydivs = soup.findAll('div')
print "OUTNAME = " + outname
f = open(outname,"w")
for div in mydivs: 
    if div:
        strDiv = str(div)
        strDiv = strDiv.replace('\n','')
        strDiv = strDiv.replace('<br/>','')
	dom2 = parseString("<root>"+strDiv+"</root>")
        div2 = dom2.getElementsByTagName("div")
        if div2 and len(div2) == 1 and div2[0] and div2[0].attributes:
            style=div2[0].getAttribute("style")
            info = "text"
            info2 = "text"
            if  style:
                #print style + "\n"
                strStyle = style.replace(' ','')
                attrs = strStyle.split(";")
                (info,info2) = parseAttrs(attrs) 
                spans =  dom2.getElementsByTagName("span")
                if spans:
                    nbspans = len(spans)
                    if nbspans == 1:                    
                        processOneSpan(spans,info,info2,f)
                    if nbspans == 2:
                        #print "nbspans = 2"
                        # format mm<space>mm<br>mm<br>mm ..
                        pos = 0
                        for theSpan in spans:
                            if pos == 0:
                                a=1
                                processFirstSpan(spans,info,info2,f)
                            pos=pos+1
                        processSecondSpan(spans,info,info2,f)

                        
f.close()




