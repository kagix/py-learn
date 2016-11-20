import sys,os,time

HOME_DIR="ratb"
CRAWL_DIR = "crawl"
TIMETABLES_DIR = "timetables"
TRIPS_DIR = "trips"
LINES_DIR = "lines"
GTFS_DIR = "gtfs"
GTFS_ROUTES = "routes.txt"
LINES_FILE = "lines.txt"
DONELINES_FILE = "donelines.txt"
PROCESSEDROUTES_FILE = "processedroutes.txt"



def getLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + LINES_FILE

def getProcessedRoutesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + PROCESSEDROUTES_FILE

def getDoneLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + DONELINES_FILE

def getRoutesPath():
    return HOME_DIR + "/" + GTFS_DIR + "/" + GTFS_ROUTES

def getTimeTablesPath(lineNumber):
    return HOME_DIR + "/" + CRAWL_DIR + "/" + TIMETABLES_DIR + "/" + str(lineNumber) + "/"

def getFirstTimeTableForLine(lineNumber):
        return "detaliu_"+str(lineNumber) + "_0.txt"


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
    f3=open(getRoutesPath(),"a") 
    f3.write( msg + "\n")
    f3.flush()
    f3.close



def processRoutes(donelines, processedroutes, routefilter):
    for doneline in donelines:
        line = doneline.strip()
        #print "DL:" + line 
        if line == "":
            continue
        #print "DL2:" + line 
        if doneline in processedroutes:
            continue
        #print "DL3:" + line 
        line = doneline.strip()
        #print "DL4:" + line 

        toks = line.split("/")
        lastok = toks[len(toks)-1].strip()
        if lastok in processedroutes:
            continue

        if len(routefilter) > 0 and lastok not in routefilter:
            print lastok + " already done" + "\n"
            continue
        print "Adding route " + lastok + "\n"
        dirname =  getTimeTablesPath(lastok)
   
        firstTimeTable = getFirstTimeTableForLine(lastok)


        for timetable in os.listdir(dirname):
           if timetable == firstTimeTable:
               fullpath=dirname+timetable
               processFirstRoute(fullpath)

        
        f = open(getProcessedRoutesPath(),"a")
        f.write(lastok + "\n")
        f.close()

def generateGTFSRoutes():
    f = open(getLinesPath(),"r")
    lines = f.readlines()
    f.close()


    f = open(getDoneLinesPath(),"r")
    donelines = f.readlines()
    f.close()


    if not os.path.exists(getProcessedRoutesPath()):
        tmp= open(getProcessedRoutesPath(),"w")
        tmp.close()

    f = open(getProcessedRoutesPath(),"r")
    processedroutes = f.readlines()
    f.close()

    numar = 0
    for line in lines:
        if line not in donelines:
    	    continue
        if line in processedroutes:
    	    continue

    f=open(getRoutesPath(),"w") 
    f.truncate()
    msg = "route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,linia,route_text_color"
    f.write( msg + "\n")
    f.flush()

    routefilter = []
    #routefilter.append("4")
    processRoutes(donelines, processedroutes, routefilter)

def main():
    generateGTFSRoutes()    
    


if __name__ == "__main__":
    main()


    
