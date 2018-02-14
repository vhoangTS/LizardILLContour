import plotly as py
import os
import plotly.graph_objs as go


def getFiles(modelpath, variantname, airnodename):
    daylightdir = os.path.join(modelpath, variantname, "Daylight")
    allills = [fname for fname in os.listdir(daylightdir) if ".ill" in fname]
    for item in allills:
        if airnodename in item:
            matchsig = item.split(".")[0]
            break
    illfile = os.path.join(daylightdir, "%s.ill" % (matchsig))
    ptsfile = os.path.join(daylightdir, "%s.pts" % (matchsig))
    return illfile, ptsfile


def readFiles(ptsfile, illfile):
    Xmatrix, Ymatrix, Zmatrix = [], [], []
    ptsf = open(ptsfile, "r")
    ptslines = ptsf.readlines()
    for line in ptslines:
        ldict = line.split()
        try:
            Xmatrix.append(float(ldict[0]))
            Ymatrix.append(float(ldict[1]))
        except TypeError:
            pass
    ptsf.close()
    illf = open(illfile, "r")
    illlines = illf.readlines()
    DA300line = illlines[-4].split()
    DA300line.pop(0)
    for item in DA300line:
        Zmatrix.append(float(item))
    illf.close()
    return Xmatrix, Ymatrix, Zmatrix


modelpath = "p:\\Milan_Focchi_Russoli_180104\\"\
            "Thermal\\20180205_Kickoff\\Model\\"
variantname = "V3_ACT_SV1_SV2"
airnodename = "OFF"

# modelpath = "c:\\Users\\vhoang\\Desktop\\LizardILLContour\\Model\\"
# variantname = "V0_DAYLIGHT"
# airnodename = "OFFICE"

illfile, ptsfile = getFiles(modelpath, variantname, airnodename)
Xmatrix, Ymatrix, Zmatrix = readFiles(ptsfile, illfile)

trace = go.Contour(
        z=Zmatrix,
        x=Xmatrix,
        x0=Xmatrix[0],
        dx=abs(Xmatrix[0]-Xmatrix[1]),
        y=Ymatrix,
        y0=Ymatrix[0],
        dy=abs(Ymatrix[0]-Ymatrix[1]),
        colorscale="Hot",
        autocontour=False,
        contours=dict(
                showlabels=True,
                start=0,
                end=100,
                size=10,
                   )
                   )
data = [trace]
layout = go.Layout(
        xaxis=dict(
                autorange=True,
                tickmode="auto",
                tick0=0,
                dtick=abs(Ymatrix[0]-Ymatrix[1]),
                domain=[min(Xmatrix), max(Xmatrix)]
                ),
        yaxis=dict(
                autorange=True,
                tickmode="auto",
                tick0=0,
                dtick=abs(Ymatrix[0]-Ymatrix[1]),
                domain=[min(Ymatrix), max(Ymatrix)]
                )
                        )
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename="test.html")
