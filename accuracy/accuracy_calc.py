#!/usr/bin/python
import sys
sys.path.append('../ulyxes/pyapi')
sys.path.append('../lib/')
import glob
from csvreader import CsvReader
import numpy as np
import math

distances = ['6m', '12m', '17m', '22m', '31m']
resolutions = ['500px', '1000px', '2000px']
measures = {}
move = {}
cols = ['hz', 'v', 'chz', 'cv', 'dist', 'type', 'datetime', 'refhz', 'refv', 'refdist']
res = np.empty((0,6))
res2 = np.empty((0,1))
for d in distances:
    measures[d] = {}
    line = np.empty((1,0))
    for r in resolutions:
        measures[d][r] = {}
        measures[d][r]['round'] = np.empty((0,8))
        measures[d][r]['mini'] = np.empty((0,8))
        measures[d][r]['mark'] = np.empty((0,8))

        print('measures/' + d + '/' + d + '_' + r + '/' + d + '_sorozat_' + r + '.csv')
        file = CsvReader(fname=glob.glob('measures/1103/' + d + '/' + d + '_' + r + '/' + d + '_sorozat_' + r + '.csv' )[0], filt=cols)
        row = file.GetNext()
        while row and row != None:
            if row['type'] != 'type':
                for e, v in row.items():
                    if v == '':
                        row[e] = '0'
                hz = float(row['hz'])*180/np.pi*3600
                v = float(row['v'])*180/np.pi*3600
                chz = float(row['chz'])*180/np.pi*3600
                cv = float(row['cv'])*180/np.pi*3600
                dist = float(row['dist'])
                refhz = float(row['refhz'])*180/np.pi*3600
                refv = float(row['refv'])*180/np.pi*3600
                refdist = float(row['refdist'])

                measures[d][r][row['type']] = np.append(measures[d][r][row['type']], [[hz, v, chz, cv, dist, refhz, refv, refdist]], axis=0)
            row = file.GetNext()

        line = np.append(line, [[np.std(measures[d][r]['mini'][:,0], ddof=1), np.std(measures[d][r]['mark'][:,0], ddof=1)]], axis=1)

    res = np.append(res, line, axis=0)

    dif = {}
    move[d] = {}
    mini = {}
    mark = {}
    move[d]['1000px'] = {}
    move[d]['1000px']['round'] = np.empty((0,10))
    move[d]['1000px']['mini'] = np.empty((0,10))
    move[d]['1000px']['mark'] = np.empty((0,10))
    try:

        file = CsvReader(fname=glob.glob('measures/1103/' + d + '/' + d + '_1000px/' + d + '_mozog_1000px.csv' )[0], filt=cols)
        print(glob.glob('measures/1103/' + d + '/' + d + '_1000px/' + d + '_mozog_1000px.csv' )[0], 'xxxx')
        row = file.GetNext()
        while row and row != None:
            if row['type'] != 'type':
                for e, v in row.items():
                    if v == '':
                        row[e] = '0'
                hz = float(row['hz'])*180/np.pi*3600
                v = float(row['v'])*180/np.pi*3600
                chz = float(row['chz'])*180/np.pi*3600
                cv = float(row['cv'])*180/np.pi*3600
                dist = float(row['dist'])
                refhz = float(row['refhz'])*180/np.pi*3600
                refv = float(row['refv'])*180/np.pi*3600
                refdist = float(row['refdist'])
                z = math.cos(float(row['v']))*float(row['dist'])
                refz = math.cos(float(row['refv']))*float(row['refdist'])

                move[d]['1000px'][row['type']] = np.append(move[d]['1000px'][row['type']], [[hz, v, chz, cv, dist, refhz, refv, refdist, z, refz]], axis=0)

            row = file.GetNext()
        move[d]['1000px']['mini']
        mini[d] = (move[d]['1000px']['mini'][:,9] - move[d]['1000px']['mini'][0,9])*1000
        mark[d] = (move[d]['1000px']['mark'][:,8] - move[d]['1000px']['mark'][0,8])*1000
        dif[d] =  mini[d] - mark[d]

        print(np.std(dif[d][1:], ddof=1))

        res2 = np.append(res2, [[np.std(dif[d][1:], ddof=1)]], axis=0)









    except:
        pass
print(res)
np.savetxt('1103_mozog.csv', res2, delimiter=';')
#np.savetxt('1103_sorozat.csv', res, delimiter=';')
