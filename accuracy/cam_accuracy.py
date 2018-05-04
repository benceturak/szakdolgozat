#!/usr/bin/python
import sys
sys.path.append('../ulyxes/pyapi')
sys.path.append('../lib/')
from camerastation import CameraStation
from totalstation import TotalStation
from remotemeasureunit  import RemoteMeasureUnit
from tcpiface import TCPIface
from leicatps1200 import LeicaTPS1200
from picameraunit import PiCameraUnit
from csvreader import CsvReader
from csvwriter import CsvWriter
from angle import Angle
import numpy as np
import cv2

if __name__ == "__main__":
    if len(sys.argv) > 3:
        ofname = sys.argv[1]
        calib_file = sys.argv[2]
        repeat = int(sys.argv[3])
    else:
        print("Usage: accuracy.py output_file calib_file repeat")
        exit()

    icols = ['hz', 'v', 'type', 'datetime', 'refhz', 'refv']
    ocols = ['hz', 'v', 'chz', 'cv', 'dist', 'type', 'datetime', 'refhz', 'refv', 'refdist']
    output = CsvWriter(fname=ofname, angle='RAD', dist='.4f', sep=";", mode='a', filt=ocols)
    inp = CsvReader(fname='ts1201.csv', filt=icols)
    rows = []
    row = inp.GetNext()


    mu = RemoteMeasureUnit()
    iface = TCPIface('test', ('192.168.1.101', 8081), timeout=25)
    #iface2 = TCPIface('test', ('192.168.1.101', 8082), timeout=25)

    class CameraStationUnit(PiCameraUnit, LeicaTPS1200): pass

    cs = CameraStation('test', mu, iface)
    #ts = CameraStation('test', mu, iface2)
    cs.LoadAffinParams(calib_file)


    while row:
        rows.append(row)
        row = inp.GetNext()

    frow = {}
    for c in ocols:
        frow[c] = c
    output.WriteData(frow)

    for i in range(0, repeat):
        #input('Press enter to start measure')
        for r in rows:

            outrow = False
            if r['type'] == 'mini':
                cs.SetATR(1)
                cs.SetPrismType(1)
                cs.Move(Angle(float(r['hz']), 'RAD'), Angle(float(r['v']), 'RAD'), 1)
                cs.Measure()
                #ts.SetATR(1)
                #ts.SetPrismType(1)
                #ts.Move(Angle(float(r['refhz']), 'RAD'), Angle(float(r['refv']), 'RAD'), 1)
                #ts.Measure()
            elif r['type'] == 'tape':
                cs.SetATR(1)
                cs.SetPrismType(2)
                cs.Move(Angle(float(r['hz']), 'RAD'), Angle(float(r['v']), 'RAD'), 1)
                cs.Measure()
                #ts.Move(Angle(float(r['refhz']), 'RAD'), Angle(float(r['refv']), 'RAD'), 1)
                #ts.SetPrismType(2)
                #ts.Measure()
            elif r['type'] == 'round':
                cs.SetATR(1)
                cs.SetPrismType(0)
                cs.Move(Angle(float(r['hz']), 'RAD'), Angle(float(r['v']), 'RAD'), 1)
                cs.Measure()
                #ts.SetATR(1)
                #ts.SetPrismType(0)
                #ts.Move(Angle(float(r['refhz']), 'RAD'), Angle(float(r['refv']), 'RAD'), 1)
                #ts.Measure()
            elif r['type'] == 'mark':
                cs.SetATR(0)
                cs.Move(Angle(float(r['hz']), 'RAD'), Angle(float(r['v']), 'RAD'), 0)
                cs.SetEDMMode('RLSTANDARD')

                outrow = cs.GetAbsAngles()

                cs.Measure()
            else:
                print('Unknown target type')
                break


            if outrow:
                dist = cs.GetMeasure()
                print(outrow)
                outrow['dist'] = dist['distance']
            else:
                outrow = cs.GetMeasure()
                #refrow = ts.GetMeasure()
                #print(refrow)
                outrow['dist'] = outrow['distance']
                #outrow['refhz'] = refrow['hz']
                #outrow['refv'] = refrow['v']
                #outrow['refdist'] = refrow['distance']

                print(outrow)
            try:
                if outrow['errorCode'] == 1285:
                    pass
                    cs.ClearDistance()
                    #ts.ClearDistance()
            except:
                pass
            outrow['type'] = r['type']


            output.WriteData(outrow)
