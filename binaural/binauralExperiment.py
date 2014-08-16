#!/usr/bin/env python

import numpy as np
import time
import os
import shutil
import logging
import pygame #audio playback
import datetime
import time

# local modules
from common import clock, draw_str
import os
from optparse import OptionParser

help_message = '''
Usage: binauralExperiment.py  [--folder <output_folder>]
'''

# This program is used to play back several binaural beats audio files for neural experiments in a timed manner.
# This version is intended to be used independently from a specific mindwave device and an appropriate capture software has to be run seperately.
if __name__ == '__main__':
    import sys, getopt
    
    of = None;
    stages = ['noise_start', 'delta', 'noise', 'theta', 'noise', 'alpha', 'noise', 'beta', 'noise', 'gamma']

    argparser = OptionParser()
    argparser.add_option("-f", "--folder", dest="foldername", help="folder to output files", default="captures")
    (options,args) = argparser.parse_args()
    print help_message
   
    pygame.init()

    # init storage directory for capture files, i.e. only current stage in csv format
    foldername = options.foldername

    dir = os.path.dirname(__file__)
    if os.path.exists(foldername):
        shutil.rmtree(foldername)
    try:
        os.mkdir(foldername)
    except:
        print "directory for capture storage not accessible."
        quit()
    of = open(foldername + "/values.csv", "w")
    of.write("time_eeg;stage;raw_eeg;delta;theta;low_alpha;high_alpha;low_beta;high_beta;low_gamma;mid_gamma;\n")

    # load background noise and open pygame audio channels
    noise_sound = pygame.mixer.Sound("data/rain2.ogg")
    channelA = pygame.mixer.Channel(1)
    channelB = pygame.mixer.Channel(2)
    channelA.play(noise_sound)
    
    # We play back noise for 2 minutes and start playing the different binaural beats layered over the initial noise afterwards (2 minutes each).
    # There is a 10 second pause between the binaural beats with the background noise playing only.
    for stage in stages:
        current_time = (datetime.datetime.now() - datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(0))).seconds #reset timer to current seconds
        timer_sec = 0
        print "capturing "+stage+" stage at time: " + str(current_time)
        binaural_sound = None
        #audio playback
        if stage is 'delta':
            binaural_sound = pygame.mixer.Sound("data/Delta(2.5Hz).ogg")
        if stage is 'theta':
            binaural_sound = pygame.mixer.Sound("data/Theta(5Hz).ogg")
        if stage is 'alpha':
            binaural_sound = pygame.mixer.Sound("data/Alpha(10Hz).ogg")
        if stage is 'beta':
            binaural_sound = pygame.mixer.Sound("data/Beta(20Hz).ogg")
        if stage is 'gamma':
            binaural_sound = pygame.mixer.Sound("data/Gamma(40.0Hz).ogg")
        if not binaural_sound is None:
            channelB.play(binaural_sound)
        else:
            channelB.stop()

        string = ""
        if stage != 'noise':
            while timer_sec <= 120:
                string = str(int(round(time.time() * 1000))) + ";" + stage + "\n"
                of.write(string)
                string = ""
                timer_sec = (datetime.datetime.now() - datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(0))).seconds - current_time
                time.sleep(0.001)
        else:
            while timer_sec <= 10:
                timestamp = int(round(time.time() * 1000))
                while timestamp - int(round(time.time())) == 0:
                    pass
                string = str(int(round(time.time() * 1000))) + ";" + stage + "\n"
                of.write(string)
                string = ""
                timer_sec = (datetime.datetime.now() - datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(0))).seconds - current_time
                time.sleep(0.001)
	
    of.close()
