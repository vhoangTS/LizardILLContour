import plotly as py
import plotly.graph_objs as go
from readb18dgeopos import *

modelpath = "c:\\Users\\vhoang\\Desktop\\LizardILLContour\\Model\\"
variantname = "V0_DAYLIGHT"
airnodename = "OFFICE"

b18file, illfile = getFiles(modelpath,variantname,airnodename)
Xmatrix,Ymatrix,dgeoslibXY = readb18(b18file)
dlres = readIllfile(illfile)
Zmatrix = getZMatrix(Xmatrix,Ymatrix,dgeoslibXY,dlres)

trace = go.Contour(z=Zmatrix,
                   x=Xmatrix,
                   y=Ymatrix,
                   colorscale = "Viridis",
                   autocontour = False,
                   contours = dict(
                           start = 0,
                           end = 100,
                           size = 10,
                   )
                   )
data = [trace]
layout = go.Layout()
fig = go.Figure(data = data, layout = layout)
py.offline.plot(fig,filename = "test.html")

