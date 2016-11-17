from bs4 import BeautifulSoup
import time
import urllib
import re
import os

def decodeMins(value):
    print( "VALUE:" + str(value))
    l = 0
    if value:
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

def removeTags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def decodeStation(table, numar,seqNo):
    dirname = "orare/linii-ore/"+str(numar)
    paragraph = table.findAll("p")
    text = str(paragraph[0])
    print text
    text = removeTags(str(paragraph[0]))
    print text
    toka=text.split(" statie = ")
    tokb=toka[1].split(" sens spre = ")
    tokc=toka[0].replace("linie = ","")
    print "LINIE:"+tokc
    print "STATIE:"+ tokb[0]
    print "DIR:"+tokb[1]
    fname = "orare/detalii/" + "detaliu_" + str(numar) + "_" + str(seqNo) + ".txt"
    fname = "detaliu_" + str(numar) + "_" + str(seqNo) + ".txt"
    fdet = open(dirname + "/" + fname,"a")
    fdet.write( "LINIA="+tokc + "\n")
    fdet.write( "STATIA="+ tokb[0] + "\n")
    fdet.write( "DIRECTIA="+tokb[1]+ "\n")
    fdet.close()
    

def decodeTable(table, numar, seq, label):
    dirname = "orare/linii-ore/"+str(numar)
    rows = table.findAll("tr")
    if len(rows) < 3:
        return
    row = rows[2]
    print str(row)
    fname = "orare/detalii/" + "detaliu_" + str(numar) + "_" + str(seqNo) + ".txt"
    fname = "detaliu_" + str(numar) + "_" + str(seqNo) + ".txt"
    print fname
    fdet = open(dirname + "/" + fname,"a")
    fdet.write(label+"\n")
    cols = row.findAll("td")
    print str(cols)
    ora = -1
    for col in cols:
        print("COL:" + str(col))
        print("VALUE:"+str(col.nodeValue))
        val2 = str(col)
        val3 = val2.replace("<br>","")
        val3 = val3.replace("<br/>","")
        print val3
        val4 = val3.replace('<td valign="top">',"")
        print val4
        val5 = val4.replace('</td>',"")
        print val5
        if ora >=0 and val5 != "":
            mins = decodeMins(val5)
            for minut in mins:
                fdet.write(str(ora) + ":" + str(minut) + "\n")
        ora = ora+1

    fdet.close()


def getSequence(name):
    return  name.split("_")[2].split(".")[0]
    
from xml.dom.minidom import parse, parseString
baseUrl = 'http://ratb.ro/pdf_statii'
f = open("linii.txt","r")
linii = f.readlines()
f.close()

if not os.path.exists("donelines.txt"):
    tmp= open("donelines.txt","a")
    tmp.close()

f2  = open("donelines.txt","r")
donelines = f2.readlines()
f2.close()

numar = 0
for linie in linii:
    if linie in donelines:
        continue

    print linie + "\n"
    tak = linie.split("/")
    numar = tak [ len(tak) -1].strip()
    print "LINIE " + numar

    links = "orare/linia_"+numar+".txt"
    fd = open(links,"r")
    detalii = fd.readlines()
    fd.close()
    dirname = "orare/linii-ore/"+str(numar)
    if not os.path.exists (dirname):
        os.mkdir(dirname)

    for detaliu in detalii:
        if "Thumbs" in detaliu:
            continue

        seqNo = getSequence(detaliu) 
        print "LINIA "+str(numar) + " SEQ "+ str(seqNo)
        urlAddress="http://ratb.ro/v_statie.php?linie="+str(numar)+"&statie=" + str(seqNo) 
        print urlAddress

        r = urllib.urlopen(urlAddress).read()
        soup = BeautifulSoup(r)
        tables = soup.findAll(['table'])

        if not tables:
            continue 

        decodeStation(tables[1], numar,seqNo)
        decodeTable(tables[2],numar, seqNo, "LUCRU")
        decodeTable(tables[3],numar, seqNo, "SAMBATA")
        decodeTable(tables[4],numar, seqNo, "DUMINICA")
        print "URMEAZA"
        time.sleep(7)

    
    f  = open("donelines.txt","a")
    f.write(linie + "\n")
    f.close()
    


