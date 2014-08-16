#!/usr/bin/env python

import numpy as np
import cv2
import time
import os
import shutil

# local modules
from video import create_capture
from common import clock, draw_str

class EyeCapture:

    video_src = None
    cascade = None
    nested = None
    glass = None
    le = None
    re = None
    cam = None
    foldername = "captures"
	
    def detect(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects

    def draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img.copy(), (x1, y1), (x2, y2), color, 2)

    def capture(self):
        string = ""
        ret, img = self.cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        t = clock()
        rects = self.detect(gray, self.cascade)
        if len(rects) == 0:
            string = str(int(round(time.time() * 1000))) + ";n.f.;"
        vis = img.copy()
        self.draw_rects(vis, rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects_fn = self.detect(roi.copy(), self.nested)
            subrects_glass = self.detect(roi.copy(), self.glass)
            subrects_le = self.detect(roi.copy(), self.le)
            subrects_re = self.detect(roi.copy(), self.re)
            string = string + str(int(round(time.time() * 1000))) + ";"
            if not len(subrects_fn) == 0:
                self.draw_rects(vis_roi, subrects_fn, (255, 0, 0))
                string = string + "1;"
            elif not len(subrects_glass) == 0:
                self.draw_rects(vis_roi, subrects_glass, (255, 0, 0))
                string = string + "1;"
            elif (not len(subrects_le) == 0) or (not len(subrects_re) == 0):
                self.draw_rects(vis_roi, subrects_le, (255, 0, 0))
                self.draw_rects(vis_roi, subrects_re, (255, 0, 0))
                string = string + "0;"
            else:
                string = string + "n.e.;"
        dt = clock() - t
	    
        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)
        cv2.imwrite(self.foldername + "/eyeCaptureImages/" + str(int(round(time.time()*1000))) + ".jpg", vis)
        return string
	
    def close(self):
        cv2.destroyAllWindows()

    def __init__(self, foldername):

        self.foldername = foldername

        cascade_fn = "haarcascades/haarcascade_frontalface_default.xml"
        nested_fn = "haarcascade_eye.xml"
        nested_glass = "haarcascades/haarcascade_eye_tree_eyeglasses.xml"
        nested_le = "haarcascades/haarcascade_lefteye_2splits.xml"
        nested_re = "haarcascades/haarcascade_righteye_2splits.xml"

        os.mkdir(self.foldername + "/eyeCaptureImages")

        print "eyeCapture: setting CascadeClassifiers"
        self.cascade = cv2.CascadeClassifier(cascade_fn)
        self.nested = cv2.CascadeClassifier(nested_fn)
        self.glass = cv2.CascadeClassifier(nested_glass)
        self.le = cv2.CascadeClassifier(nested_le)
        self.re = cv2.CascadeClassifier(nested_re)
		
        self.cam = create_capture(0)
