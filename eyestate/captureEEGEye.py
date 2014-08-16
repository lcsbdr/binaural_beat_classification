#!/usr/bin/env python

import numpy as np
import cv2
import time
import os
import shutil
import logging

# local modules
from video import create_capture
from common import clock, draw_str
import eegCapture
import eyeCapture
import os
import time
from optparse import OptionParser

help_message = '''
USAGE: captureEEGEye.py  [--folder <output_folder>]
'''

if __name__ == '__main__':
    import sys, getopt
    print help_message

    of = None;

    argparser = OptionParser()
    argparser.add_option("-f", "--folder", dest="foldername", help="folder to output files", default="captures")
    (options,args) = argparser.parse_args()

    foldername = options.foldername

    dir = os.path.dirname(__file__)
    if os.path.exists(foldername):
        shutil.rmtree(foldername)
    try:
        os.mkdir(foldername)
    except:
        print "directory for eyeCapture file stores not accessible."
        quit()
    of = open(foldername + "/values.csv", "w")
    of.write("time_start;time_eye;eyestate;time_eeg;raw_eeg\n")

    print "initializing EEG..."
    rawEEG = eegCapture.RawDataPlotting(foldername)
    print "initializing camera..."
    camera = eyeCapture.EyeCapture(foldername)

    print "creating threads..."

    try:
        print "start capturing, close with escape."
        string = ""
        while True:
            if 0xFF & cv2.waitKey(5) == 27:
                break
            string = str(int(round(time.time() * 1000))) + ";" + rawEEG.getData() + camera.capture() + "\n"
            of.write(string)
            string = ""
	
        of.close()
        print "visualizing rawEEG data..."
        rawEEG.visualize()
        print "closing camera..."
        camera.close()

    except Exception as ex:
        logging.exception("exception triggered, getting the fuck out of here...")
        rawEEG.close()
        camera.close()
        quit()
    
	
