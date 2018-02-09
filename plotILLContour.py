import plotly as py
import plotly.graph_objs as go
from readb18dgeopos import *

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

modelpath = "p:\\Milan_Focchi_Luxottica_180103\\Thermal\\20180126_KickOff\\Model\\20170208\\"
variantname = "V0_ALLAIR"
airnodename = "OFF"

#modelpath = "c:\\Users\\vhoang\\Desktop\\LizardILLContour\\Model\\"
#variantname = "V0_DAYLIGHT"
#airnodename = "OFFICE"

illfile,ptsfile = getFiles(modelpath, variantname, airnodename)
Xmatrix,Ymatrix,Zmatrix = readFiles(ptsfile, illfile)
mindomain = min(min(Xmatrix), min(Ymatrix))
maxdomain = max(max(Xmatrix),max(Ymatrix))

trace = go.Contour(
        z= Zmatrix,
        x= Xmatrix,
        x0= Xmatrix[0],
        dx= abs(Xmatrix[0]-Xmatrix[1]),
        y=  Ymatrix,
        y0= Ymatrix[0],
        dy= abs(Ymatrix[0]-Ymatrix[1]),
        colorscale = "Hot",
        autocontour = False,
        contours = dict(
                start = 0,
                end = 100,
                size = 10,
                   )
                   )
data = [trace]
layout = go.Layout(
        xaxis = dict(
                autorange = False,
                tickmode = "auto",
                tick0 = 0,
                dtick = abs(Ymatrix[0]-Ymatrix[1]),
                domain = [mindomain,maxdomain]
                ),
        yaxis = dict(
                autorange = False,
                tickmode = "auto",
                tick0 = 0,
                dtick = abs(Ymatrix[0]-Ymatrix[1]),
                domain = [mindomain,maxdomain]
                )
                        )
fig = go.Figure(data = data, layout = layout)
#py.offline.plot(fig,filename = "test.html")

