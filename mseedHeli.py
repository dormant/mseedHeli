#!/usr/bin/env python
# plot_heli_mseed.py
#
# Recreates a helicorder plot using obspy for every 24-hour mseed file in the current directory
# Use this command to copy files
# $ find /mnt/mvohvs3/MVOSeisD6/mseed/MV -type f -name '2023.109.*Z.mseed' -print0 | xargs -0 cp --target-directory=.
#
# R.C. Stewart, 24-December-2021
#
import os
import sys
import glob
import argparse
import re
import obspy
from datetime import datetime, date, timedelta
from dateutil import parser as dparser
from dateutil.rrule import rrule, DAILY
from obspy.core import UTCDateTime, Stream



for filename in os.listdir("."):
    if filename.endswith(".msd") or filename.endswith(".mseed"): 

        print( filename )

        secInDay = 60*60*24
        filenameSeparator = "."
        dirnameSeparator = "/"

        chunks = filename.split( '.' )
        year = chunks[0]
        doy = chunks[1]
        sta = chunks[3]
        net = chunks[2]
        loc = chunks[4]
        cha = chunks[5]
	
        loc = loc if loc else '--'

        st = obspy.read( filename )

        scnl = '_'.join( [ sta, cha, net, loc ] )

        date = UTCDateTime( ''.join( [ str(year), str(doy).zfill(3) ] ), iso8601=True )

        title = '   '.join( [ scnl, date.strftime( "%Y %m %d" ) ] )
        filePlot = '.'.join( [ scnl, date.strftime( "%Y%m%d00a" ), 'png' ] )

        if sta == 'MSS1':
            vsr = 1500
        elif sta == 'MBHA':
            vsr = 500
        elif sta == 'MBLG':
            vsr = 10000
        elif sta == 'MBLY':
            vsr = 10000
        elif sta == 'MBRV':
            vsr = 2500
        elif sta == 'MBRY':
            vsr = 5000
        elif cha == 'HHZ': 
            vsr = 10000
            #vsr = 20000
        elif cha == 'HH1': 
            vsr = 20000
        elif cha == 'HH2': 
            vsr = 20000
        elif cha == 'BHZ':
            vsr = 10000
        else:
            vsr = 3000
    
        st.plot(type='dayplot',
            interval=15,
            right_vertical_labels=False,
            one_tick_per_line=False,
           # size=(852,1500), 
            size=(1278,1500), 
            title=title, 
            vertical_scaling_range=vsr,
            tick_format='%H:%M', 
            outfile=filePlot, 
            color=['k', 'r', 'b', 'g'], 
            linewidth=0.3)


