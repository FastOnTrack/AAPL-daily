from flask import Flask
from flask import render_template
app = Flask(__name__)
import StringIO
import base64
# import matplotlib.pyplot as plt
import urllib2
import time
import numpy
from numpy import exp, cos, linspace
import bokeh.plotting as plt
import os, re

@app.route('/')
def test():

    img = StringIO.StringIO()
    ## TIME
    date = time.strftime("%d-%b-%Y")
    filename = 'AAPL prices ' + date
    print "Created file: " + filename
    print time.strftime("%c")
    print " "

    unixday = 0
    INTERVAL = 150
    ### CAN COMMENT THIS BLOCK OUT aesthetic purposes x-axis Unix time fix -> 390 to 780
    from time import mktime
    from datetime import date
    start = date(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")))
    unixday = mktime(start.timetuple())

    ## take from google API exercise using d c o p v for different amount of loadtxt progression
    counter = 0
    # while counter < 3:
    url = 'http://www.google.com/finance/getprices?i=61&p=1d&f=d,c,h,v&df=cpct&q=AAPL'
    webContent = urllib2.urlopen(url).read()
    f = open(filename, 'w')
    f.write(webContent.replace("a", ""))
    f.close
    f = open(filename, 'r')
    ## DATA -- probably will switch to pandas library if problems in progression occur
    x, y = numpy.loadtxt(open(filename), delimiter=',', skiprows=7, usecols=(0,1), unpack=True)
    print 'Minute Progression: ' + str(len(x))
    f.close # this one may not be right if need to data troubleshoot
    ## MOVING AVERAGE change INTERVAL to 60, 75, or 100
    yMA = numpy.convolve(y, numpy.ones(INTERVAL)/INTERVAL, 'valid')
    sigma = numpy.std(y)

    ## PLOTTING
    x = (x - unixday)/60/60
    plt.plot(x[len(y)-len(yMA):],yMA)
    plt.plot(x,y)
    plt.title(time.strftime("%c"))
    plt.xlabel('Hour')
    plt.ylabel('Price $')

    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue())
    print "For", time.strftime("%d-%b-%Y")
    print "AAPL average:", sum(y)/len(y)
    print "AAPL std dev:", sigma
    print "AAPL price", y[-1]

    return render_template('test.html', plot_url=plot_url)
