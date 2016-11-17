from bs4 import BeautifulSoup
import urllib
from xml.dom.minidom import parse, parseString
baseUrl = 'http://ratb.ro/pdf_statii'
r = urllib.urlopen(baseUrl).read()
soup = BeautifulSoup(r)
#print type(soup)
active = 0
anchors = soup.findAll(['a', 'href'])
#print str(anchors)
if  anchors == None:
    print "No data. Exiting ...\n"
    exit
href = ""
linii = []
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
        if href == "1/":
            print  "Activating...\n" 
            active = 1
        if active == 0:
            print  "Skipping...\n" 
            continue
        print str(href) + "\n" 
        linii.append(str(href).split('/')[0])

f = open("linii","w")

for linie in linii:
    f.write(baseUrl+"/"+linie + "\n")

f.close()
    
    


