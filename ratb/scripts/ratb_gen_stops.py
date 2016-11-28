import sys,os,time

HOME_DIR="ratb"
CRAWL_DIR = "crawl"
TIMETABLES_DIR = "timetables"
TRIPS_DIR = "trips"
LINES_DIR = "lines"
GTFS_DIR = "gtfs"
GTFS_STOPS = "stops.txt"
LINES_FILE = "lines.txt"
DONELINES_FILE = "donelines.txt"
PROCESSEDSTOPS_FILE = "processedstops.txt"
STOPS_DIR = "stops"

HEADER = "stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon"

STOPS_TRAMWAY= "stops_linii_tramvai.csv"
LINES_TRAMWAY = "linii_tramvai.csv"

STOPS_TROLLEYBUS= "stops_linii_troleibuz.csv"
LINES_TROLLEYBUS = "linii_troleibuz.csv"


STOPS_AUTOBUZ = "stops_autobuz.csv"
LINES_AUTOBUZ =       "linii_autobuz.csv"


STOPS_EXPRES = "stops_linii_expres.csv"
LINES_EXPRES =       "linii_expres.csv"


STOPS_PREORAS = "stops_linii_preorasenesti.csv"
LINES_PREORAS =       "linii_preorasenesti.csv"


LINEFILTER="linefilter.txt"

filteredlines=[]

def getLineFilterPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + LINEFILTER



def getLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + LINES_FILE

def getStopsPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + STOPS_DIR 

def getTramwayStopsPath():
    return getStopsPath() + "/" + STOPS_TRAMWAY

def getTramwayLineStopsPath():
    return getStopsPath() + "/" + LINES_TRAMWAY

def getTrolleybusStopsPath():
    return getStopsPath() + "/" + STOPS_TROLLEYBUS

def getTrolleybusLineStopsPath():
    return getStopsPath() + "/" + LINES_TROLLEYBUS


def getAutobusStopsPath():
    return getStopsPath() + "/" + STOPS_AUTOBUZ

def getAutobusLineStopsPath():
    return getStopsPath() + "/" + LINES_AUTOBUZ



def getPreorasStopsPath():
    return getStopsPath() + "/" + STOPS_PREORAS

def getPreorasLineStopsPath():
    return getStopsPath() + "/" + LINES_PREORAS

def getExpresStopsPath():
    return getStopsPath() + "/" + STOPS_EXPRES

def getExpresLineStopsPath():
    return getStopsPath() + "/" + LINES_EXPRES


def getProcessedStopsPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + PROCESSEDSTOPS_FILE

def getDoneLinesPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + LINES_DIR + "/" + DONELINES_FILE

def getGTFSStopsPath():
    return HOME_DIR + "/" + GTFS_DIR + "/" + GTFS_STOPS

def tokenizeConnexions(connexions):
    toks = connexions.replace(" ","").split(";")
    result = []
    for tok in toks:
        if tok:
            result.append(tok)

    return result

def tokenizeLineStopEntry(entry):
    toks= entry.strip().split('\"')
    conex = toks[1].replace(",",";").replace(" ","")
    toks1 = toks[0].split(",")
    lineseq = toks1[0].split("_")

   
    result = []
    result.append(lineseq[0]) # line
    result.append(lineseq[1]) # seq
    result.append(toks[2].replace(",",""))    # up/down
    result.append(toks1[1])   # name  
    result.append(toks1[2])   # stop code/id
    result.append(tokenizeConnexions(conex))      # list of connexions
    return result 
    

def readTramwayLineStops():
    f = open(getTramwayLineStopsPath(),"r")
    stops = f.readlines()
    f.close()

    lineNumber = 0

    tramwayLineStops = {}
    for entry in stops:  
        if lineNumber  > 0:
        
            tokens = tokenizeLineStopEntry(entry)
            tramwayLineStops[tokens[4]] = tokens
        lineNumber = lineNumber +1 
 
    return tramwayLineStops

def readLineStops(path):
    f = open(path,"r")
    stops = f.readlines()
    f.close()

    lineNumber = 0

    tramwayLineStops = {}
    for entry in stops:  
        if lineNumber  > 0:
        
            tokens = tokenizeLineStopEntry(entry)
            tramwayLineStops[tokens[4]] = tokens
        lineNumber = lineNumber +1 
 
    return tramwayLineStops

def tokenizeStopEntry(entry):
    toks = entry.strip().split(',')

    result = []
    result.append(toks[0])    # stop code
    result.append(toks[1])    # long
    result.append(toks[2])    # lat
    result.append(toks[3])    # name
    return result 

def readTramwayStops():
    f = open(getTramwayStopsPath(),"r")
    stops = f.readlines()
    f.close()

    lineNumber = 0

    tramwayStops = {}
    for entry in stops:  
        if lineNumber  > 0:
        
            #print entry 
            tokens = tokenizeStopEntry(entry)
            tramwayStops[tokens[0]] = tokens
        lineNumber = lineNumber +1 
 
    return tramwayStops

def readStops(path):
    f = open(path,"r")
    stops = f.readlines()
    f.close()

    lineNumber = 0

    tramwayStops = {}
    for entry in stops:  
        if lineNumber  > 0:
        
            #print entry 
            tokens = tokenizeStopEntry(entry)
            tramwayStops[tokens[0]] = tokens
        lineNumber = lineNumber +1 
 
    return tramwayStops
def generateStopData(stopId, stopCode, stopName, stopDesc, stopLat, stopLong):
    stopData = []
    stopData.append(stopId) # 0
    stopData.append(stopCode) # 1
    stopData.append(stopName) #2
    stopData.append(stopDesc) #2
    stopData.append(stopLat)  #3
    stopData.append(stopLong) #4
    return stopData

def getValidStopPosition(stops, lineStops, name):
    for key in lineStops:
        if lineStops[key][3] != name:
            continue
        #print lineStops[key]
        code = lineStops[key][4]
        #print "Code = " + code
        if stops[code][1] != "" and stops [code][2] != "":
            #print stops[code][1]  + "," [code][2] 
            return (stops[code][1],stops [code][2])
    return ("","")

def generateStops(stops, pathStops, pathLineStops):
    
    global filteredlines
    ret = {}
    for k in stops:
        if k not in ret:
            ret[k] = stops[k]
    tramwayLineStops = readLineStops(pathLineStops)
    tramwayStops = readStops(pathStops)
   
    tramwayLines = []
    skipIt = 1
    for key in tramwayStops:
        if key in tramwayLineStops:
            if key in stops:
                continue
            stopInfo = tramwayStops[key]     
            lineStopInfo = tramwayLineStops[key]   
            if 1 == 1:
                skipIt = 1
                # tramwayLines[0] in lineStopInfo[5]:
                # statia e pe linia tramvaiului
                stopId = key
                stopCode = key
                stopName = stopInfo[3]
               
                stopDesc = "Statie comuna pentru liniile : "
                if len(lineStopInfo[5]) == 1:
                    stopDesc = "Statie izolata de pe traseul liniei "
                for tram in lineStopInfo[5]:
                    stopDesc = stopDesc + " " + tram
                    if len(filteredlines) == 0 or tram in filteredlines:
                        #print "Will add station " + stopName
                        skipIt = 0
                stopLat = stopInfo[2]
                stopLong = stopInfo[1]
                if skipIt == 0:
                    #print "Long:"+stopLong + "   Lat:" + stopLat
                    if stopLong == "" and stopLat == "":
                        #print "Stop " + stopName + " does not have GPS position. Looking around"
                        (lon,lat)  = getValidStopPosition(tramwayStops, tramwayLineStops,stopName)
                        stopLong = lon
                        stopLat = lat
                        if stopLong != "" and stopLat != "":
                            if 1 == 0:
                                print "Stop " + stopName + " has now a GPS position."
                        else:
                            print stopDesc
                            print "Stop " + stopName + " has no GPS position."

                #stopData = []
                #stopData.append(stopId) # 0
                #stopData.append(stopCode) # 1
                #stopData.append(stopName) #2
                #stopData.append(stopDesc) #2
                #stopData.append(stopLat)  #3
                #stopData.append(stopLong) #4
                stopData = generateStopData(stopId, stopCode, stopName, stopDesc, stopLat, stopLong)
                if skipIt == 0: 
                    #print "Adding stop " + stopData[2]
                    stops[key] =stopData 
                    ret[key] =stopData 

    return ret



def writeKeys(stops):

    f = open(getGTFSStopsPath(),"a")
    for key in stops:
        stopData = stops[key]
        stopEntry = ""
        stopEntry = stopEntry       + stopData[0] 
        stopEntry = stopEntry + "," + stopData[1] 
        stopEntry = stopEntry + "," + stopData[2] 
        stopEntry = stopEntry + "," + stopData[3] 
        stopEntry = stopEntry + "," + stopData[4] 
        stopEntry = stopEntry + "," + stopData[5] 
        f.write(stopEntry+ "\n") 
    f.close()


def generateGTFSStops():
    global filteredlines
    stops = {}
    f = open(getLineFilterPath(),"r")
    filteredlines = f.readlines()
    f.close()

    f = open(getLineFilterPath(),"r")
    flines = f.readlines()
    for l in flines:
        filteredlines.append(l.strip())
    f.close()

    stops = generateStops(stops, getTramwayStopsPath(),getTramwayLineStopsPath())
    stops = generateStops(stops, getTrolleybusStopsPath(),getTrolleybusLineStopsPath())
    stops = generateStops(stops, getAutobusStopsPath(),getAutobusLineStopsPath())
    stops = generateStops(stops, getPreorasStopsPath(),getPreorasLineStopsPath())
    stops = generateStops(stops, getExpresStopsPath(),getExpresLineStopsPath())

    f = open(getGTFSStopsPath(),"a")
    f.truncate()
    f.write(HEADER+ "\n")
    f.close()

    writeKeys(stops)
 

    

    f.close()


def main():
    generateGTFSStops()    
    


if __name__ == "__main__":
    main()


