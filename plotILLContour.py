import plotly as py
import plotly.graph_objs as go
from readb18dgeopos import *

modelpath = "c:\\Users\\vhoang\\Desktop\\LizardILLContour\\Model\\"
variantname = "V0_DAYLIGHT"
airnodename = "OFFICE"

b18file, illfile = getFiles(modelpath,variantname,airnodename)
Xmatrix,Ymatrix,dgeoslibXY = readb18(b18file)
mindomain = min(min(Xmatrix), min(Ymatrix))
maxdomain = max(max(Xmatrix),max(Ymatrix))
dlres = readIllfile(illfile)
Zmatrix = getZMatrix(Xmatrix,Ymatrix,dgeoslibXY,dlres)


trace = go.Contour(
        z= Zmatrix,
        x= Xmatrix,
        #x0= Xmatrix[0],
        #dx= abs(Xmatrix[0]-Xmatrix[1]),
        y=  Ymatrix,
        #y0= Ymatrix[0],
        #dy= abs(Ymatrix[0]-Ymatrix[1]),
        colorscale = "YlOrRd",
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
                #tick0 = 0,
                #dtick = abs(Ymatrix[0]-Ymatrix[1]),
                #domain = [mindomain,maxdomain]
                ),
        yaxis = dict(
                autorange = False,
                tickmode = "auto",
                #tick0 = 0,
                #dtick = abs(Ymatrix[0]-Ymatrix[1]),
                #domain = [mindomain,maxdomain]
                )
                        )
fig = go.Figure(data = data, layout = layout)
py.offline.plot(fig,filename = "test.html")

