import sys,os,time

def getTransportTypeName(number):
    ret = "tramvai"
    if  number < 60:
        ret = "tramvai"
    if  number > 60 and number < 100:
        ret = "troleibuz"
    if  number > 100 and number < 400:
        ret = "autobuz urban"
    if  number > 600 and number < 700:
        ret = "autobuz urban"
    if  number > 400 and number < 500:
        ret = "autobuz preorasenesc"
    if  number > 500 and number < 600:
        ret = "autobuz de noapte"
    if  number > 700 and number < 800:
        ret = "expres"
    return ret

  
def getTransportType(number):
    ret = 0
    if  number < 60:
        ret = 0
    if  number > 60 and number < 100:
        ret = 3
    if  number > 100 and number < 400:
        ret = 3
    if  number > 600 and number < 700:
        ret = 3
    if  number > 400 and number < 500:
        ret = 3
    if  number > 500 and number < 600:
        ret = 3
    if  number > 700 and number < 800:
        ret = 3
    return ret

def getRouteUrl(number):
    ret = "http://ratb.ro/"
    if  number < 60:
        ret = ret + "v_tramvai.php?tlin1=" +str(number)
    if  number > 60 and number < 100:
        ret = ret + "v_troleibuz.php?tlin1=" +str(number)
    if  number > 100 and number < 400:
        ret = ret + "v_bus_urban.php?tlin1=" +str(number)
    if  number > 600 and number < 700:
        ret = ret + "v_bus_urban.php?tlin1=" +str(number)
    if  number > 400 and number < 500:
        ret = ret + "v_bus_preorasenesc.php?tlin1=" +str(number)
    if  number > 500 and number < 600:
        ret = ret + "v_bus_urban.php?tlin1=" +str(number)
    if  number > 700 and number < 800:
        ret = ret + "v_bus_expres.php?tlin1=" +str(number)
    return ret


 

def processFirstRoute(filename):
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
    lucru=""
    sambata=""
    duminica=""
   
    
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
    	    lucru="LUCRU"
    	    continue
    
        if "SAMBATA" in line:
    	    sambata="SAMBATA"
    	    continue
    
        if "DUMINICA" in line:
    	    duminica="DUMINICA"
    	    continue
    
        
    
    msg=str(linia) + "," 
    msg = msg +  "RATB" + ","
    msg = msg + str(linia)+","
    msg = msg + "Linia de " + getTransportTypeName(int(linia)) + " intre statiile " + statia + " si " + directia + ","
    msg = msg + "Circula in zile de " + lucru + " " + sambata + " " + duminica + ","
    msg = msg + str(getTransportType(int(linia))) + ","
    msg = msg + getRouteUrl(int(linia)) + ","
    msg = msg + "FF0000" + ","
    msg = msg + "FFFFFF"
    f3=open("routes.csv","a") 
    f3.write( msg + "\n")
    f3.flush()
    f3.close

def processRoutes(donelines, processedroutes):
    for doneline in donelines:
        
        line = doneline.strip()
        if line == "":
            continue
        if doneline in processedroutes:
            continue
        line = doneline.strip()

        toks = line.split("/")
        lastok = toks[len(toks)-1].strip()
        if lastok in processedroutes:
            continue

        dirname = "orare/linii-ore/"+lastok + "/"
   
        fnam = "detaliu_"+str(lastok) + "_0.txt"
        for timetable in os.listdir(dirname):
           if timetable == fnam:
               fullpath=dirname+timetable
               processFirstRoute(fullpath)

        
        f  = open("processedroutes.txt","a")
        f.write(lastok + "\n")
        f.close()

def main():
    f = open("linii.txt","r")
    linii = f.readlines()
    f.close()
    
    f = open("donelines.txt","r")
    donelines = f.readlines()
    f.close()
    
    if not os.path.exists("processedroutes.txt"):
        tmp= open("processedroutes.txt","a")
        tmp.close()
    f2  = open("processedroutes.txt","r")
    processedroutes = f2.readlines()
    f2.close()
    numar = 0
    for linie in linii:
        if linie not in donelines:
    	    continue
        if linie in processedroutes:
    	    continue
    f3=open("routes.csv","w") 
    msg = "route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,linia,route_text_color"
    f3.write( msg + "\n")
    f3.flush()
    processRoutes(donelines, processedroutes)

if __name__ == "__main__":
    main()


    
