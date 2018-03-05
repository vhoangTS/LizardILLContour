import plotly as py
import os
import sys
import plotly.graph_objs as go


def getFiles(modelpath, variantname, airnodename):
    daylightdir = os.path.join(modelpath, variantname, "Daylight")
    allills = [fname for fname in os.listdir(daylightdir) if ".ill" in fname]
    matchsig = None
    for item in allills:
        if airnodename in item:
            matchsig = item.split(".")[0]
            break
        else:
            pass
    if matchsig == None:
        # print "*.ill file not found!"
        sys.exit("*.ill file not found!")
    else:
        illfile = os.path.join(daylightdir, "%s.ill" % (matchsig))
        ptsfile = os.path.join(daylightdir, "%s.pts" % (matchsig))
    return illfile, ptsfile


def readFiles(plotmode, ptsfile, illfile):
    Xmatrix, Ymatrix, Zmatrix = [], [], []
    # get X, Y coordinate
    ptsf = open(ptsfile, "r")
    ptslines = ptsf.readlines()
    for line in ptslines:
        ldict = line.split()
        try:
            Xmatrix.append(round(float(ldict[0]),2))
            Ymatrix.append(round(float(ldict[1]),2))
        except TypeError:
            pass
    ptsf.close()
    # read *ill file
    illf = open(illfile, "r")
    illlines = illf.readlines()
    DA300line = illlines[-4].split()
    DA300line.pop(0)
    DFline = illlines[-1].split()
    DFline.pop(0)
    if plotmode == "DA":
        for item in DA300line:
            Zmatrix.append(round(float(item),2))
    elif plotmode == "DF":
        for item in DFline:
            Zmatrix.append(round(float(item),2))
    illf.close()
    return Xmatrix, Ymatrix, Zmatrix


def plotting(plotmode, connectmode, Xmatrix, Ymatrix, Zmatrix, vname):
    if plotmode == "DF":
        title = "Daylight Factor"
        endscale = 6
        stepscale = 1
        color = "Jet"
    elif plotmode == "DA":
        title = "Daylight Autonomy"
        endscale = 100
        stepscale = 10
        color = "Jet"
    imgsiz = 1600
    xdis = abs(max(Xmatrix) - min(Xmatrix))
    ydis = abs(max(Ymatrix) - min(Ymatrix))
    ratio = ydis / xdis
    trace = go.Contour(
            z=Zmatrix,
            x=Xmatrix,
            x0=Xmatrix[0],
            dx=abs(Xmatrix[0]-Xmatrix[1]),
            y=Ymatrix,
            y0=Ymatrix[0],
            dy=abs(Ymatrix[0]-Ymatrix[1]),
            colorscale=color,
            connectgaps=connectmode,
            autocontour=False,
            colorbar=dict(
                    title=title,
                    titleside='right',
                    titlefont=dict(size=min(imgsiz/100, 16)),
                    ),
            contours=dict(
                    coloring='heatmap',
                    showlabels=True,
                    labelfont=dict(size=min(imgsiz/100, 16)),
                    start=0,
                    end=endscale,
                    size=stepscale,
                    ),
            line=dict(
                color='rgb(0, 0, 0)',
                smoothing=0.85,
                dash='dot',
                width=1),
                    )
    data = [trace]
    layout = go.Layout(
            title="%s - %s" % (title, vname),
            xaxis=dict(
                    autorange=True,
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    tickmode="auto",
                    #tick0=0,
                    #dtick=abs(Xmatrix[0]-Xmatrix[1]),
                    #domain=[min(Xmatrix), max(Xmatrix)]
                    ),
            yaxis=dict(
                    autorange=True,
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    tickmode="auto",
                    #tick0=0,
                    #dtick=abs(Ymatrix[0]-Ymatrix[1]),
                    #domain=[min(Ymatrix), max(Ymatrix)]
                    )
                        )
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(
        fig,
        filename="%s_%s.html" % (vname, plotmode),
        image='png',
        image_filename="%s_%s" % (vname, plotmode),
        image_width=imgsiz,
        image_height=ratio * imgsiz,
        )


modelpath = "c:\\Users\\vhoang\\Desktop\\test\\Model\\"
variantname = ["BASIS0"]
airnodename = "Z1"
plotmode = ["DF", "DA"]  # DF: Daylight Factor, DA: Daylight Autonomy
connectmode = False # still very confusing, True if the shape is rectangular, false if the shape is complicated??
for vname in variantname:
    for plotm in plotmode:
        illfile, ptsfile = getFiles(modelpath, vname, airnodename)
        Xmatrix, Ymatrix, Zmatrix = readFiles(plotm, ptsfile, illfile)
        plotting(plotm, connectmode, Xmatrix, Ymatrix, Zmatrix, vname)
