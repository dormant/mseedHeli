#!/usr/bin/env python
# plot_heli_mseed.py
#
# Recreates a spectrogram plot using obspy for every 24-hour mseed file in the current directory
# Use this command to copy files
# $ find /mnt/mvohvs3/MVOSeisD6/mseed/MV -type f -name '2023.109.*Z.mseed' -print0 | xargs -0 cp --target-directory=.
#
# R.C. Stewart, 22-June-2023
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
        filePlot = '.'.join( [ scnl, date.strftime( "%Y%m%d00" ), 'png' ] )

        tr = st[0];
        tr.detrend( 'demean' );
        tr.filter("highpass", freq=1.0)
        t = tr.stats.starttime
        tr.trim(t,t+6*60*60)
        fs = tr.stats.sampling_rate
        tr.spectrogram( outfile=filePlot,
                       title=title,
                       dbscale=False,
                       cmap='jet',
                       wlen=1024/fs,
                       )


