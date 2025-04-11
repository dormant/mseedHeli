#!/usr/bin/env python
# mseedHeliNoFrills.py
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
import subprocess



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

        date = UTCDateTime( ''.join( [ str(year), str(doy).zfill(3) ] ), iso8601=True )

        if sta == 'MSS1':
            vsr = 1500
        elif sta == 'MBHA':
            vsr = 500
        elif sta == 'MBLG':
            vsr = 10000
        elif sta == 'MBLY':
            vsr = 10000
        elif sta == 'MBRV':
            vsr = 500
        elif sta == 'MBRY':
            vsr = 5000
        elif sta == 'MBWH':
            vsr = 2500
        elif cha == 'HHZ': 
            vsr = 10000
        elif cha == 'BHZ':
            vsr = 10000
        else:
            vsr = 3000

        st.merge(method=-1)
        tr = st[0]
        tr.detrend( 'demean' )
        #print( tr.stats.npts )
        if cha == 'HHZ':
            st.filter("highpass", freq=1.0)
            cha = 'EHZ'
        elif cha == 'BHZ':
            st.filter("highpass", freq=1.0)
            cha = 'SHZ'
        tr.stats.channel = cha
        sc = '_'.join( [ sta, cha ] )
        filePlot = '.'.join( [ sc, date.strftime( "%Y%m%d" ), 'png' ] )


        try:
            tr.plot(type='dayplot',
                starttime=date,
                endtime=date + secInDay,
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
            #print( 'Helicorder generated', filePlot, sep=': ' )
        except:
            print( 'Helicorder not generated - exception' )



command = 'mogrify -crop 911x1015+145+63 *.png'
subprocess.run(command, shell = True, executable="/usr/bin/bash")
