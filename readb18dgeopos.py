import os
import re

def getFiles(modelpath,variantname,airnodename):
    b18file = os.path.join(modelpath,variantname,"%s.b18"%(variantname))
    #illfile = os.path.join(modelpath,variantname,"Daylight\\006_%s.ill"%(airnodename))
    daylightdir = os.path.join(modelpath,variantname,"Daylight")
    allills = [fname for fname in os.listdir(daylightdir) if ".ill" in fname]
    for item in allills:
        if airnodename in item:
            matchsig = item.split(".")[0]
            break
    illfile = os.path.join(daylightdir,"%s.ill"%(matchsig))
    ptsfile = os.path.join(daylightdir,"%s.pts"%(matchsig))
    return illfile,ptsfile

def readFiles(ptsfile, illfile):
    Xmatrix,Ymatrix,Zmatrix = [],[],[]
    ptsf = open(ptsfile,"r")
    ptslines = ptsf.readlines()
    for line in ptslines:
        ldict = line.split()
        try:
            Xmatrix.append(float(ldict[0]))
            Ymatrix.append(float(ldict[1]))
        except:
            pass
    ptsf.close()
    illf = open(illfile,"r")
    illlines = illf.readlines()
    DA300line = illlines[-4].split()
    DA300line.pop(0)
    for item in DA300line:
        Zmatrix.append(float(item))
    illf.close()
    return Xmatrix, Ymatrix, Zmatrix
