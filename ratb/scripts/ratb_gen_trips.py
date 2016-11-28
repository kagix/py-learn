import sys,os,time

HOME_DIR="ratb"
CRAWL_DIR = "crawl"
TIMETABLES_DIR = "timetables"
TRIPS_DIR = "trips"
LINES_DIR = "lines"
GTFS_DIR = "gtfs"
GTFS_TRIPS = "trips.txt"
TRIPS_FILE = "trips.txt"
DONELINES_FILE = "donelines.txt"
PROCESSEDTRIPS_FILE = "processedtrips.txt"
LINES_FILE = "lines.txt"

LINEFILTER="linefilter.txt"

filteredlines=[]

def getLineFilterPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + LINEFILTER

def getLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + LINES_FILE

def getDoneLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + DONELINES_FILE

def getTimeTablesPath(lineNumber):
    return HOME_DIR + "/" + CRAWL_DIR + "/" + TIMETABLES_DIR + "/" + str(lineNumber) + "/"

def getTripNumberPath(lineNumber):
    return HOME_DIR + "/" + CRAWL_DIR + "/" + TRIPS_DIR + "/" + "linia_" + str(lineNumber) + ".txt"


def getTripsPath():
    return HOME_DIR + "/" + GTFS_DIR + "/" + GTFS_TRIPS

def getProcessedTripsPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + PROCESSEDTRIPS_FILE

def readDoneLines():
    f = open(getDoneLinesPath(), "r")
    content = f.readlines()
    f.close()
    return content

def getFirstTimeTableForLine(lineNumber, direction):
    if direction == "up":
        return "detaliu_"+str(lineNumber) + "_0.txt"
    if direction == "down":
        return "detaliu_"+str(lineNumber) + "_50.txt"


def processFirstTrip(filename, dircode):
    f = open(filename,'r')
    lines = f.readlines()
    f.close
    
    f3=open(getTripsPath(),"a") 
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
   
    number=0
    day=""   
       
    code="" 
    cal=""

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
            cal="CAL12345"
            day="L"
            number = 0
    	    continue
    
        if "SAMBATA" in line:
    	    sambata="SAMBATA"
            cal="CAL6"
            day="S"
            number = 0
    	    continue
    
        if "DUMINICA" in line:
    	    duminica="DUMINICA"
            cal="CAL7"
            day="D"
            number = 0
    	    continue

        toks = line.strip().split(":")
        if len(toks) == 2:
            code=str(linia)+"_"+day+ "_" + dircode + "_" + str(number)
            number = number+1 
            msg=str(linia) + "," + str(cal)  + "," + code
            
            msg=str(linia) + "," 
            msg = msg +  str(cal) + ","
            msg = msg + str(code)
            f3.write( msg + "\n")

        f3.flush()
        f3.close

def processFirstTripUp(filename):
    processFirstTrip(filename,"U")

def processFirstTripDown(filename):
    processFirstTrip(filename,"D")

def processTrips(donelines, processedtrips, tripfilter):
    for doneline in donelines:
        line = doneline.strip()
        if line == "":
            continue
        if doneline in processedtrips:
            continue
        line = doneline.strip()

        toks = line.split("/")
        lastok = toks[len(toks)-1].strip()
        if lastok in processedtrips:
            continue

        if len(tripfilter) > 0 and lastok not in tripfilter:
            print lastok + " already done" + "\n"
            continue
        print "Adding trip " + lastok + "\n"
        dirname =  getTimeTablesPath(lastok)


        firstTimeTableUp = getFirstTimeTableForLine(lastok, "up")
        firstTimeTableDown = getFirstTimeTableForLine(lastok, "down")

        for timetable in os.listdir(dirname):
           if timetable == firstTimeTableUp:
               fullpath=dirname+timetable
               processFirstTripUp(fullpath)
           if timetable == firstTimeTableDown:
               fullpath=dirname+timetable
               processFirstTripDown(fullpath)

def generateGTFSTrips():
    f = open(getLineFilterPath(),"r")
    filteredlines = f.readlines()
    f.close()

    print "Generate trips"
    f = open(getLinesPath(),"r")
    lines = f.readlines()
    f.close()

    f = open(getDoneLinesPath(),"r")
    donelines = f.readlines()
    f.close()

    if not os.path.exists(getProcessedTripsPath()):
        tmp= open(getProcessedTripsPath(),"w")
        tmp.close()

    f = open(getProcessedTripsPath(),"r")
    processedtrips = f.readlines()
    f.close()


    f=open(getTripsPath(),"w") 
    f.truncate()
    msg = "route_id,service_id,trip_id"
    f.write( msg + "\n")
    f.flush()
    f.close()

    tripfilter = []
    for l in filteredlines:
        tripfilter.append(l.strip())
    processTrips(donelines, processedtrips, tripfilter)




def main():
    generateGTFSTrips()    
    


if __name__ == "__main__":
    main()


