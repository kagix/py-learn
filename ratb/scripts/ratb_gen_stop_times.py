import sys,os,time

HOME_DIR="ratb"
CRAWL_DIR = "crawl"
TIMETABLES_DIR = "timetables"
TRIPS_DIR = "trips"
LINES_DIR = "lines"
GTFS_DIR = "gtfs"
GTFS_STOP_TIMES = "stop_times.txt"
DONELINES_FILE = "donelines.txt"
PROCESSEDTRIPS_FILE = "processedtrips.txt"
LINES_FILE = "lines.txt"

CRAWL_STOPS_DIR="stops"

CRAWL_LINE_BUS="linii_autobuz.csv"
CRAWL_LINE_TRAMWAY="linii_tramvai.csv"
STOPS="stops"
COUNT="count"
TIMES="times"
TRIPS="trips"
STOP_CODE="code"
KEY_LUCRU="L"
KEY_SAMBATA="S"
KEY_DUMINICA="D"

LINENO="4"

LINEFILTER="linefilter.txt"

filteredlines=[]

def getLineFilterPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + LINEFILTER


def getLinesTramwayPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + CRAWL_STOPS_DIR + "/" + CRAWL_LINE_TRAMWAY

def getLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + LINES_FILE

def getDoneLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + DONELINES_FILE

def getTimeTablesPath(lineNumber):
    return HOME_DIR + "/" + CRAWL_DIR + "/" + TIMETABLES_DIR + "/" + str(lineNumber) + "/"

def getTripNumberPath(lineNumber):
    return HOME_DIR + "/" + CRAWL_DIR + "/" + TRIPS_DIR + "/" + "linia_" + str(lineNumber) + ".txt"

def getStopTimesPath():
    return HOME_DIR + "/" + GTFS_DIR + "/" + GTFS_STOP_TIMES


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

def readTimeTableFile(filePath):
    timeTable={}

    f = open(filePath,'r')
    lines = f.readlines()
    f.close
   
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
        sline = line.strip()
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
            day=KEY_LUCRU
            number = 0
            timeTable[day] = []
    	    continue
    
        if "SAMBATA" in line:
    	    sambata="SAMBATA"
            cal="CAL6"
            day=KEY_SAMBATA
            timeTable[day] = []
            number = 0
    	    continue
    
        if "DUMINICA" in line:
    	    duminica="DUMINICA"
            cal="CAL7"
            day=KEY_DUMINICA
            timeTable[day] = []
            number = 0
    	    continue

        toks = line.strip().split(":")
        toks.append("00")
        if len(toks) == 3:
            if len(timeTable[day]) < 100:
                timeTable[day].append(":".join(toks))

    return timeTable


def readTimeTableForLine(lineNumber):
    timeTable = {}
    dirPath = getTimeTablesPath(lineNumber)
    for fileName in os.listdir(dirPath):
        fullPath = dirPath + fileName

        split1 = fileName.split(".")
        if split1[0] == "":
            continue
        table = readTimeTableFile(fullPath)
        split2 = split1[0].split("_")
        timeTable[split2[2]] = table
    return timeTable     

def readTramwayStops():
    f = open(getLinesTramwayPath(),"r")
    data = f.readlines()
    f.close()
    #stops[<1>|<4>|<..>][<up>|<down>]["trips"|"stops"]
    # trips -> [trip_no][seq_no]=ora
    # stops -> seq_no ->infos
    
    stops = {}
    num = 0
    for detail in data:
        if num > 0:
            toks = detail.split(",")
            (line,seq)=toks[0].strip().split("_")
            #if not line  == LINENO:
            #    continue
            cod = toks[2].strip()
            direction=toks[len(toks)-1].strip()
            #if not line == LINENO:
            #    continue 
            if line not in stops.keys():
                stops[line] = {}
            if direction not in stops[line].keys():
                stops[line][direction] = {}
                stops[line][direction][STOPS] = {}
            # increase count    
            if seq not in stops[line][direction][STOPS].keys():
                stops[line][direction][STOPS][int(seq)]={}
            stops[line][direction][STOPS][int(seq)][STOP_CODE]=cod
 
        num = num + 1
    return stops
        
def getDirection(direction):
    if direction == "up":
        return "U"
    else:
        return "D"

def plotStopTimes(stopTimes):
    lista = [];
    f=open(getStopTimesPath(),"a") 
    for line in stopTimes.keys():
        for direction in stopTimes[line].keys():
            #if direction== "down":
            #    continue
            stops  = stopTimes[line][direction][STOPS].keys()
            print str(stopTimes[line][direction][STOPS].keys())
            for stop in stopTimes[line][direction][STOPS].keys():
                stopStr = str (stop)
                if TIMES not in stopTimes[line][direction].keys():
                    continue
                for day in stopTimes[line][direction][TIMES][stopStr].keys():
                    #for trip in stopTimes[line][direction][TIMES][stopStr][day]:
                    #print (""+line + "/"+direction + "/"+ stopStr+ "/" + day + "/" + str(trip))
                    nbTrips = len(stopTimes[line][direction][TIMES][stopStr][day])
                    for tripNo in range(0,nbTrips):
                        tripId = line + "_" + day + "_" + getDirection(direction) + "_" + str(tripNo)
                        arrivalTime = stopTimes[line][direction][TIMES][stopStr][day][tripNo]
                        departureTime = stopTimes[line][direction][TIMES][stopStr][day][tripNo]
                        stopId = stopTimes[line][direction][STOPS][stop] ['code']
                        stopSequence = stopStr
                        msg = tripId + "," + arrivalTime+ "," + departureTime + "," + stopId + "," + stopSequence
                        #print msg
                        f.write(msg + "\n")
    f.close()
    


def appendLineTable(lineNo, stops):
    tramStops = stops 
    global filteredlines
    print(str(filteredlines))    
    if lineNo not in filteredlines:
        return tramStops   
    table = readTimeTableForLine(lineNo)
    direction=""
    for key in table.keys():
        ikey = int(key)
        if ikey >= 50:
            direction="down"
            ikey = ikey-50
        else:
            direction="up"
        if not TIMES  in tramStops[lineNo][direction].keys():
            tramStops[lineNo][direction][TIMES]= {}
        tramStops[lineNo][direction][TIMES][str(ikey)]= table[key]
    return tramStops

def generateGTFSStopTimes():
    f = open(getLineFilterPath(),"r")
    global filteredlines
    flines = f.readlines()
    for l in flines:
        filteredlines.append(l.strip())
    f.close()

    tramStops = readTramwayStops()
    print str(tramStops)
    tramStops = appendLineTable("1",tramStops)
    tramStops = appendLineTable("4",tramStops)
    tramStops = appendLineTable("5",tramStops)
    tramStops = appendLineTable("7",tramStops)
    tramStops = appendLineTable("8",tramStops)
    tramStops = appendLineTable("10",tramStops)
    tramStops = appendLineTable("11",tramStops)
    tramStops = appendLineTable("14",tramStops)
    tramStops = appendLineTable("16",tramStops)
    tramStops = appendLineTable("21",tramStops)
    tramStops = appendLineTable("23",tramStops)
    tramStops = appendLineTable("24",tramStops)
    tramStops = appendLineTable("25",tramStops)
    tramStops = appendLineTable("27",tramStops)
    tramStops = appendLineTable("32",tramStops)
    tramStops = appendLineTable("35",tramStops)
    tramStops = appendLineTable("36",tramStops)
    tramStops = appendLineTable("40",tramStops)
    tramStops = appendLineTable("41",tramStops)
    
    f=open(getStopTimesPath(),"w") 
    f.truncate()
    msg = "trip_id,arrival_time,departure_time,stop_id,stop_sequence"
    f.write( msg + "\n")
    f.flush()
    f.close()

    plotStopTimes(tramStops)

def main():
    generateGTFSStopTimes()    
    


if __name__ == "__main__":
    main()


