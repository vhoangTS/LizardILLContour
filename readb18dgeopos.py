import os
import re

def getFiles(modelpath,variantname,airnodename):
    b18file = os.path.join(modelpath,variantname,"%s.b18"%(variantname))
    illfile = os.path.join(modelpath,variantname,"Daylight\\001_%s.ill"%(airnodename))
    return b18file,illfile

def getDataParagraph(startpattern,stoppattern,datararray):
    """by Mark Sen Dong for TRNLizard b18 geometry visualization
    Get paragraph between start and stop pattern"""
    output = []
    inparagraph = 'FALSE'
    lines=datararray
    for i in range(len(lines)):
        search_start=re.search(r'{0}'.format(startpattern),lines[i])
        if search_start is not None or inparagraph == 'TRUE':
            inparagraph = 'TRUE'
            lines[i] = lines[i].split('\n')[0]
            if lines[i].startswith('*'):
                pass
            else:
                output.append(lines[i])
            search_stop=re.search(r'{0}'.format(stoppattern),lines[i])
            if search_stop is not None:
                return output
                pass

def readb18(b18file):
    b18 = open(b18file,"r")
    b18data = b18.readlines()
    dgeoposblock = getDataParagraph("_EXTENSION_DaylightSensorPoints_START_","_EXTENSION_DaylightSensorPoints_END_",b18data)
    #dgeoslib = dict()
    dgeoslibXY = dict()
    Xmatrix, Ymatrix = [],[]
    for line in dgeoposblock:
        if "dgeopos" in line:
            nline = line.split()
            #dgeoslib[int(nline[1])] = [float(nline[2]),float(nline[3]),float(nline[4])]
            dgeoslibXY[int(nline[1])] = [float(nline[2]),float(nline[3])]
            if float(nline[2]) not in Xmatrix:
                Xmatrix.append(float(nline[2]))
            if float(nline[3]) not in Ymatrix:
                Ymatrix.append(float(nline[3]))
    b18.close()
    return Xmatrix,Ymatrix,dgeoslibXY

def readIllfile(illfile):
    ill = open(illfile,"r")
    illdata = ill.readlines()
    dlres = dict()
    n0line = illdata[0].split()
    n0line.pop(0)
    for line in illdata:
        if "DA_300" in line and "CDA_300" not in line:
            daline = line.split()
            daline.pop(0)
            #print(daline)
            for id,value in enumerate(daline):
                dlres[int(n0line[id])] = float(value)
    ill.close()
    return dlres

def getZMatrix(Xmatrix,Ymatrix,dgeoslibXY,dlres):
    Zmatrix = list()
    for idy,yvalue in enumerate(Ymatrix):
        dummy = []
        for idx,xvalue in enumerate(Xmatrix):
            XY = [xvalue,yvalue]
            for ptsID in dgeoslibXY.keys():
                if dgeoslibXY[ptsID] == XY:
                    dummy.append(dlres[ptsID])
            pass
        Zmatrix.append(dummy)
    return Zmatrix




