import mindwave, time
import pygame,sys
import matplotlib.pyplot as plt


class RawDataPlotting:

    raw_d=[]
    ts = []
    headset = 0
    run_it=1
    foldername = "captures"

    def __init__(self, foldername):
        self.foldername = foldername
        time.sleep(2)
        #pygame.init()
        self.headset = mindwave.Headset('/dev/ttyUSB0','ee69')
        #pygame.display.set_mode((100,100))
        self.headset.connect()
        print "Connecting..."
        
        while self.headset.status != 'connected':
            time.sleep(0.5)
            if self.headset.status == 'standby':
                self.headset.connect()
            print "Retrying connect..."
        print "Connected."

    def close(self):
        print "closing headset..."
        self.headset.disconnect()

    def getData(self, limit=500000):
        string = ""
        string = str(int(round(time.time()*1000))) + ";"
        if self.headset.raw_data < limit:
            string = string + str(self.headset.raw_data) + ";"
            self.raw_d.append(self.headset.raw_data)
        else:
            string = string + "0;"
        return string

    def visualize(self):
        print "finished"

        x= range(0,len(self.raw_d))
        plt.figure()
        plt.plot(x,self.raw_d,'r')
        plt.show()
