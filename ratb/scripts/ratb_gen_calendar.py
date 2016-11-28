import sys,os,time

HOME_DIR="ratb"
CRAWL_DIR = "crawl"
CALENDAR_DIR = "calendar"
CALENDAR_PROPS = "calendar.props"
GTFS_DIR = "gtfs"
GTFS_CALENDAR = "calendar.txt"

def getPropsPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + CALENDAR_DIR + "/" + CALENDAR_PROPS

def getCalendarPath():
    return HOME_DIR + "/" + GTFS_DIR + "/" + GTFS_CALENDAR


def genDefProps():
    properties = {}
    properties["ID"] = "service_id"
    properties["MONDAY"] = "monday"
    properties["TUESDAY"] = "tuesday"
    properties["WEDNESDAY"] = "wednesday"
    properties["THURSDAY"] = "thursday"
    properties["FRIDAY"] = "friday"
    properties["SATURDAY"] = "saturday"
    properties["SUNDAY"] = "sunday"
    properties["START"] = "start_date"
    properties["END"] = "end_date"
    return properties 

def readProps(path):
    propsFile = open(path)
    lines = propsFile.readlines()
    propsFile.close()

    properties = {}
    propset={}
    id=""
    for line in lines:
        tokens = line.strip().split("=")
        if len(tokens) >= 2:
            key = tokens[0].strip()
            value = tokens[1].strip()
            if key:
                if key == "ID":
                    id = value
                    propset={}
                propset[key] = value
                if key == "END":
                    properties[id] = propset
                    propset = {}

    print str(properties)
    return properties 

def genProps(defProps, calendarProps):

    print "-----------------\n"
    print str(defProps) + "\n"
    print str(calendarProps) + "\n"
    print "-----------------\n"
    header = ""
    body =[]
    for cal in calendarProps.keys():
        line = ""
        print "cal:" + str(cal) 
        
        header = ""
        for key in calendarProps[cal]: 
            if key in defProps:
                if header:
                    header = header + ","
                if line:
                    line = line + ","
                header = header + defProps[key]
                line  = line + calendarProps[cal][key]
        body.append(line)
         
    
    return (header,body)


def writeHeaderBodyFile(header,body,path):
    file = open(path,"w")
    file.write(header + "\n")
    for line in body:
	file.write(line + "\n" )
    file.close()

def generateGTFSCalendar():
    propsPath = getPropsPath()
    props = readProps(propsPath)
    (header,body) = genProps(genDefProps(),props)
    print str(header)
    print str(body)
    writeHeaderBodyFile(header,body,getCalendarPath()) 


def main():
    generateGTFSCalendar()

if __name__ == "__main__":
    main()


    
