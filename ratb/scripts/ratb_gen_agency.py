import sys,os,time

HOME_DIR="ratb"
CRAWL_DIR = "crawl"
AGENCY_DIR = "agency"
AGENCY_PROPS = "agency.props"
GTFS_DIR = "gtfs"
GTFS_AGENCY = "agency.txt"

def getPropsPath():
    return HOME_DIR + "/" + CRAWL_DIR + "/" + AGENCY_DIR + "/" + AGENCY_PROPS

def getAgencyPath():
    return HOME_DIR + "/" + GTFS_DIR + "/" + GTFS_AGENCY


def genDefProps():
    properties = {}
    properties["ID"] = "agency_id"
    properties["NAME"] = "agency_name"
    properties["URL"] = "agency_url"
    properties["TIMEZONE"] = "agency_timezone"
    properties["LANG"] = "agency_lang"
    properties["PHONE"] = "agency_phone"
    properties["FARE_URL"] = "agency_fare_url"
    properties["EMAIL"] = "agency_email"
    return properties 

def readProps(path):
    propsFile = open(path)
    lines = propsFile.readlines()
    propsFile.close()

    properties = {}
    for line in lines:
        tokens = line.strip().split("=")
        if len(tokens) >= 2:
            key = tokens[0].strip()
            value = tokens[1].strip()
            properties[key] = value

    return properties 

def genProps(defProps, agencyProps):
    header = ""
    body = ""

    for key in agencyProps:
        if key in defProps:
            if header:
                header = header + ","
            if body:
                body = body + ","
            header = header + defProps[key]
            body  = body + agencyProps[key]
    return (header,body)


def writeHeaderBodyFile(header,body,path):
    file = open(path,"w")
    file.write(header + "\n")
    file.write(body )
    file.close()

def generateGTFSAgency():
    propsPath = getPropsPath()
    props = readProps(propsPath)
    (header,body) = genProps(genDefProps(),props)
    writeHeaderBodyFile(header,body,getAgencyPath()) 


def main():
    generateGTFSAgency()

if __name__ == "__main__":
    main()


    
