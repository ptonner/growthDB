import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import datetime
import random

from .models import *

import pandas as pd

def parse_time(t):
    import time

    try:
        return time.struct_time(time.strptime(t,'%H:%M:%S'))
    except ValueError, e:
        try:
            t = time.strptime(t,'%d %H:%M:%S')
            t = list(t)
            t[2]+=1
            return time.struct_time(t)
        except ValueError, e:
            raise Exception("Time format unknown")

def handle_data(p):

    import datetime
    import numpy as np

    print dir(p.dataFile)

    data = pd.read_csv(p.dataFile)

    assert data.columns[0].lower() == "time"
    data = data.drop("Blank",1)

    def convert_time(x):
        delta = datetime.datetime(*x[:-2]) - datetime.datetime(*t[0][:-2])
        return 24*delta.days + float(delta.seconds)/3600

    t = data.iloc[:,0].apply(parse_time)
    t = t.apply(convert_time).round(2)
    data['Time'] = t

    data.iloc[:,1:] = np.log(data.iloc[:,1:])
    data.iloc[:,1:] = data.iloc[:,1:] - data.iloc[0,1:]

    return data

def plate_plot(p):

    data = handle_data(p)

    ylim = (data.iloc[:,1:].values.min(),data.iloc[:,1:].values.max())

    cmap = plt.get_cmap("spectral")
    buff = .05

    experimentalDesigns = list(p.experimentalDesigns())
    label = [str(ed) for ed in experimentalDesigns] + ["None"]

    s = 4
    ncol = 4
    nrow = (len(experimentalDesigns)+1)/ncol+1
    fig=Figure(figsize=(s*ncol,s*nrow),tight_layout=True)

    for i in range(1,data.shape[1]):
        w = Well.objects.get(number=data.columns[i],plate=p)

        if w.experimentalDesign:
            ind = experimentalDesigns.index(w.experimentalDesign)
        else:
            ind = len(experimentalDesigns)

        ax=fig.add_subplot(nrow,ncol,ind+1)

        l = ""
        if label[ind]:
            l = label[ind]
            label[ind] = None

        # if ind < len(experimentalDesigns):
        if len(experimentalDesigns) > 0:
            cnum = (1. - 2*buff)*(ind+1)/len(experimentalDesigns) + buff
        else:
            cnum = 0
        ax.plot(data.iloc[:,0],data.iloc[:,i],color=cmap(cnum),label=l,linewidth=2,alpha=.5)
        ax.set_ylim(ylim)


    for i in range(len(experimentalDesigns)):
        ax=fig.add_subplot(nrow,ncol,i+1)
        ax.set_title(",\n".join(str(experimentalDesigns[i]).split(",")),fontsize=15)

        if (i+1) % ncol == 1:
            ax.set_ylabel("log(od)",fontsize=15)
        if (i+1) > (nrow-1)*ncol:
            ax.set_xlabel("time (h)",fontsize=15)
        

    i = len(experimentalDesigns)+1
    ax = fig.add_subplot(nrow,ncol,len(experimentalDesigns)+1)
    ax.set_title("none",fontsize=15)
    # ax.set_xlabel("time (h)",fontsize=20)
    # ax.set_ylabel("log(od)",fontsize=20)
    if (i+1) % ncol == 1:
        ax.set_ylabel("log(od)",fontsize=15)
    if (i+1) > (nrow-1)*ncol:
        ax.set_xlabel("time (h)",fontsize=15)

    return fig

def plate_canvas(p):

    fig = plate_plot(p)
    canvas=FigureCanvas(fig)

    return canvas

def save_plate_image(plate):
    from StringIO import StringIO
    from io import BytesIO
    from django.core.files import File
    from django.core.files.base import ContentFile

    # fig = plate_plot(plate)
    canvas = plate_canvas(plate)
    f = BytesIO()
    canvas.print_png(f)

    content_file = ContentFile(f.getvalue())
    plate.image.save(plate.name+'.png', content_file)
    plate.save()
