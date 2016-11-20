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


def processStopTimesForRouteAndDirection(filename, number,dircode, stops):
    stopTimes = stops
    split1 = filename.split(".")
    split2 = split1[0].split("_")
    split2[len(split2)-1]=""
    prefix="_".join(split2)
    
    delta = 0
    if dircode =="down":
        delta=50

    for key in stopTimes[number][dircode].keys():
        if key == COUNT:
            continue
        ikey = int(key)
        iname=ikey + delta
          
        

    f = open(filename,'r')
    lines = f.readlines()
    f.close
    
    #f3=open(getTripsPath(),"a") 
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
            code=str(number)+"_"+day+ "_" + dircode + "_" + str(number)
            number = number+1 
            msg=str(linia) + "," + str(cal)  + "," + code
            
            msg=str(linia) + "," 
            msg = msg +  str(cal) + ","
            msg = msg + str(code)
            print msg
            #f3.write( msg + "\n")

        #f3.flush()
        #f3.close

def processStopTimesUp(filename, number):
    return processStopTimesForRouteAndDirection(filename,number,"U", stops)

def processStopTimesDown(filename, number,stops):
    return processStopTimesForRouteAndDirection(filename,number,"D", stops)

def processStopTimes(donelines, filter, stops):
    stopTimes = stops
    for doneline in donelines:
        line = doneline.strip()
        if line == "":
            continue
        line = doneline.strip()

        toks = line.split("/")
        lastok = toks[len(toks)-1].strip()

        if len(filter) > 0 and lastok not in filter:
            #print lastok + " already done" + "\n"
            continue
        print "Adding trip " + lastok + "\n"
        dirname =  getTimeTablesPath(lastok)


        firstTimeTableUp = getFirstTimeTableForLine(lastok, "up")
        firstTimeTableDown = getFirstTimeTableForLine(lastok, "down")

        for timetable in os.listdir(dirname):
           if timetable == firstTimeTableUp:
               fullpath=dirname+timetable
               stopTimes = processStopTimesUp(fullpath, lastok, stopTimes)

           if timetable == firstTimeTableDown:
               fullpath=dirname+timetable
               stopTimes = processStopTimesDown(fullpath, lastok, stopTimes)
    return stopTimes

def readTramwayStops():
    f = open(getLinesTramwayPath(),"r")
    data = f.readlines()
    f.close()
    stops = {}
    num = 0
    for detail in data:
        if num > 0:
            toks = detail.split(",")
            (line,seq)=toks[0].strip().split("_")
            cod = toks[2].strip()
            direction=toks[len(toks)-1].strip()
            if line not in stops.keys():
                stops[line] = {}
            if direction not in stops[line].keys():
                stops[line][direction] = {}
                stops[line][direction][COUNT] = 0
                stops[line][direction][STOPS] = {}
            # increase count    
            if seq not in stops[line][direction][STOPS].keys():
                if (int(seq) +1) > stops[line][direction][COUNT]:
                    stops[line][direction][COUNT]=(int(seq) +1)
                stops[line][direction][int(seq)]={}
                stops[line][direction][int(seq)]['']={}
                stops[line][direction][int(seq)]={}
  
 
        num = num + 1
    return stops
        


def generateGTFSStopTimes():
    tramStops = readTramwayStops()
    print str(tramStops['4'])
    print "Generate stop times"
    f = open(getLinesPath(),"r")
    lines = f.readlines()
    f.close()

    f = open(getDoneLinesPath(),"r")
    donelines = f.readlines()
    f.close()



    f=open(getStopTimesPath(),"w") 
    f.truncate()
    msg = "trip_id,arrival_time,departure_time,stop_id,stop_sequence"
    f.write( msg + "\n")
    f.flush()
    f.close()

    filter = []
    filter.append("4")
    processStopTimes(donelines,  filter, tramStops)




def main():
    generateGTFSStopTimes()    
    


if __name__ == "__main__":
    main()


