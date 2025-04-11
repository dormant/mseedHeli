#!/usr/bin/env python
# mseedHeliNoFrills2.py
#
# Recreates a helicorder plot using obspy for certain stations for one day
#
# R.C. Stewart, 09-July-2024
#
import os
import sys
import glob
import argparse
import re
import obspy
import warnings
from datetime import datetime, date, timedelta
from dateutil import parser as dparser
from dateutil.rrule import rrule, DAILY
from obspy.core import UTCDateTime, Stream
import subprocess
from obspy.clients.filesystem.sds import Client as sdsClient
from obspy.clients.earthworm import Client


secInDay = 60*60*24
filenameSeparator = "."
dirnameSeparator = "/"
clientTimeout = 20


############  Arguments
parser = argparse.ArgumentParser( prog='mseedHeliNoFrills.py', description='Plot raw helicorders for certain stations', usage='%(prog)s [options]',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 epilog = 'Example:  mseedHeliNoFrills.py --date yesterday' )
choices=['wws','mseed']
parser.add_argument('-s', '--source', default='mseed', help='Data source: '+' | '.join(choices), metavar='')
parser.add_argument('-y', '--yesterday', action='store_true', help='Set date to yesterday')
parser.add_argument('-t', '--today', action='store_true', help='Set date to today')
parser.add_argument('-d', '--date', default='today', help='Date of event (UTC): today | yesterday | yyyy-mm-dd | yyyy.jjj', metavar='')
args = parser.parse_args()

dataSource= args.source
eventDate = args.date
setToday = args.today
setYesterday = args.yesterday


############  Sort out dates and times
today = datetime.utcnow().date()
if eventDate == 'yesterday' or setYesterday:
    dateBeg = UTCDateTime(today.year, today.month, today.day) - secInDay
elif eventDate == 'today' or setToday:
    dateBeg = UTCDateTime(today.year, today.month, today.day)
else:
    dateBeg = dparser.parse(eventDate)



wwsIP = '172.17.102.60'
wwsPort = 16022
pathMseed = '/mnt/mvohvs3/MVOSeisD6/mseed'


dateEnd = dateBeg + timedelta(hours=24)
print( dateBeg )
print( dateEnd )
year=dateBeg.year

stations= ["MSS1","MBBY","MBFL","MBFR","MBGH","MBLG","MBLY","MBRV","MBRY","MBWH"]
net = "MV"



for sta in stations:
    print(sta)

    if sta == "MSS1":
        cha = "SHZ"
        loc = ""
        vsr = 1500
    if sta == "MBBY":
        cha = "HHZ"
        loc = "00"
        vsr = 10000
    if sta == "MBFL":
        cha = "HHZ"
        loc = "00"
        vsr = 10000
    if sta == "MBFR":
        cha = "HHZ"
        loc = "00"
        vsr = 10000
    if sta == "MBGB":
        cha = "HHZ"
        loc = "00"
        vsr = 10000
    if sta == "MBGH":
        cha = "HHZ"
        loc = "00"
        vsr = 10000
    if sta == "MBLG":
        cha = "HHZ"
        loc = "00"
        vsr = 10000
    if sta == "MBLY":
        cha = "HHZ"
        loc = "00"
        vsr = 10000
    elif sta == "MBHA":
        cha = "SHZ"
        loc = ""
        vsr = 500
    elif sta == "MBRV":
        cha = "BHZ"
        loc = ""
        vsr = 500
    elif sta == "MBRY":
        cha = "BHZ"
        loc = ""
        vsr = 5000
    elif sta == "MBWH":
        cha = "BHZ"
        loc = ""
        vsr = 2500


    if dataSource == 'wws':
        client = Client(wwsIP, wwsPort, clientTimeout)
        info = client.get_availability(network=net, station=sta, channel=cha)
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        st = client.get_waveforms(net, sta, loc, cha, dateBeg, dateEnd)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    elif dataSource == 'mseed':
        warnings.filterwarnings("ignore")
        client = sdsClient(dirnameSeparator.join([pathMseed, net]))
        client.FMTSTR = '{station}/{year}.{doy:03d}.{network}.{station}.{location}.{channel}.mseed'
        st = client.get_waveforms(net, sta, loc, cha, dateBeg, dateEnd)
        warnings.filterwarnings("default")


    if len(st) > 0:
        st.merge(method=-1)
        tr = st[0]
        tr.detrend( 'demean' )
        print( tr.stats.npts )
        if cha == 'HHZ':
            tr.filter("highpass", freq=1.0)
            cha = 'EHZ'
        elif cha == 'BHZ':
            tr.filter("highpass", freq=1.0)
            cha = 'SHZ'
        tr.stats.channel = cha
        sc = '_'.join( [ sta, cha ] )
        filePlot = '.'.join( [ sc, dateBeg.strftime( "%Y%m%d" ), 'png' ] )


        try:
            tr.plot(type='dayplot',
                starttime=dateBeg,
                endtime=dateEnd,
                interval=15,
                right_vertical_labels=False,
                one_tick_per_line=False,
                size=(1200,1200), 
                vertical_scaling_range=vsr,
                tick_format='%H:%M', 
                outfile=filePlot, 
                color=['k', 'k', 'k', 'k'], 
                linewidth=0.5,
                number_of_ticks=1)
        except:
            print( 'Helicorder not generated - exception' )
    else:
        print( 'Helicorder not generated - no data' )



command = 'magick mogrify -crop 911x1015+145+63 M*.png'
subprocess.run(command, shell = True, executable="/usr/bin/bash")

command = 'mv M*.png /mnt/mvofls2/Seismic_Data/monitoring_data/helicorder_plots_raw/' + str( year )
subprocess.run(command, shell = True, executable="/usr/bin/bash")
