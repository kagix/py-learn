from bs4 import BeautifulSoup
import time
import urllib
from xml.dom.minidom import parse, parseString
baseUrl = 'http://ratb.ro/pdf_statii'
f = open("linii.txt","r")
linii = f.readlines()
f.close()
numar = 0
for linie in linii:
    #time.sleep(5)
    print linie + "\n"
    tak = linie.split("/")
    numar = tak [ len(tak) -1].strip()
    print "LINIE " + numar
    r = urllib.urlopen(linie).read()
    soup = BeautifulSoup(r)
    active = 0
    anchors = soup.findAll(['a', 'href'])
    #print str(anchors)
    if  anchors == None:
        print "No data. Exiting ...\n"
        exit
    href = ""
    time.sleep(3)
    statii = []
    for anchor in anchors:
    	href = ""
    	strAnchor = str(anchor)
    	print strAnchor
    	dom2 = parseString("<root>"+strAnchor+"</root>")
    	print str(dom2)
    	anc = dom2.getElementsByTagName("a")
    	print str(anc)
    	if anc and anc[0] and  anc[0].getAttribute('href'):
    	    href = anc[0].getAttribute("href")
    	if not href:
    	    print  "Null href...\n" 
    	    continue
    	if ".pdf" in href:
    	    print  "Activating...\n" 
    	    active = 1
    	if active == 0:
    	    print  "Skipping...\n" 
    	    continue
    	print str(href) + "\n" 
    	statii.append(str(href))

        fname = "linia_"+numar+".txt"
        print "FNAME=" + fname
        fl = open(fname,"w")

        for statie in statii:
            fl.write(baseUrl+"/" + str(numar) + "/"+statie + "\n")
        
        fl.close()
    
    


