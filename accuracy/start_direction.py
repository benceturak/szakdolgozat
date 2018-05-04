import sys
sys.path.append('../ulyxes/pyapi')
sys.path.append('../lib/')
from totalstation import TotalStation
from tcpiface import TCPIface
from leicatps1200 import LeicaTPS1200
from remotemeasureunit import RemoteMeasureUnit
from csvwriter import CsvWriter


iface = TCPIface('iface', ("192.168.1.101", 8081), timeout=25)
mu = RemoteMeasureUnit()




ts = TotalStation('station1', mu, iface)

cols = ['hz', 'v', 'type', 'datetime']

csv = CsvWriter(fname='ts1201.csv', angle='RAD', dist='.4f', sep=";", mode='w+', filt=cols)
frow = {}
for c in cols:
    frow[c] = c
csv.WriteData(frow)
del frow
while True:
    type = input('Target type:' )
    if type == '':
        break
    row = ts.GetAngles()
    row['type'] = type
    csv.WriteData(row)

#ts.SetATR(0)
#ts.SetEDMMode('RLSTANDARD')
#print(ts.GetPrismType())
#print(ts.SetPrismType(4))
##input('target on the marker')
#ts.GetAngles()

#input('target on the prism')
