import sys,os,time



def processTimeTable(filename):
    f = open(filename,'r')
    lines = f.readlines()
    f.close
    
    parts = filename.split("/")
    part = parts [ len(parts) -1]

    parts = part.split(".")
    part = parts[0]
    parts = part.split("_")
    part = parts[2]
 
    linia=""
    statia=""
    directia=""
    zi=""
    ora=""
   
    
    for line in lines:
        if "LINIA=" in line:
       	    linia=line.split("=")[1].strip()
    	    continue
    
        if "STATIA=" in line:
            statia=line.split("=")[1].strip()
    	    continue
    
        if "DIRECTIA=" in line:
    	    directia=line.split("=")[1].strip()
    	    continue
    
        if "LUCRU" in line:
    	    zi="LUCRU"
    	    continue
    
        if "SAMBATA" in line:
    	    zi="SAMBATA"
    	    continue
    
        if "DUMINICA" in line:
    	    zi="DUMINICA"
    	    continue
        
        ora = line.strip()
        msg=linia+","+part+","+statia+","+directia+","+zi + "," + ora.strip() 
        f3.write( msg + "\n")
    f3.close

def processLines(donelines, processedlines):
    for doneline in donelines:
        
        line = doneline.strip()
        if line == "":
            continue
        if doneline in processedlines:
            continue
        line = doneline.strip()

        toks = line.split("/")
        lastok = toks[len(toks)-1].strip()
        if lastok in processedlines:
            continue

        dirname = "orare/linii-ore/"+lastok + "/"
   
        for timetable in os.listdir(dirname):
           if timetable.startswith("detaliu_"): 
               fullpath=dirname+timetable
               processTimeTable(fullpath)

        
        f  = open("processedlines.txt","a")
        f.write(lastok + "\n")
        f.close()


f = open("linii.txt","r")
linii = f.readlines()
f.close()

f = open("donelines.txt","r")
donelines = f.readlines()
f.close()

if not os.path.exists("processedlines.txt"):
    tmp= open("processedlines.txt","a")
    tmp.close()

f2  = open("processedlines.txt","r")
processedlines = f2.readlines()
f2.close()

numar = 0
for linie in linii:
    if linie not in donelines:
        continue
    if linie in processedlines:
        continue

f3=open("timetable.csv","a") 
msg = "linia,nr_statie,statia,directia,ziua,ora"
f3.write( msg + "\n")

processLines(donelines, processedlines)


    
