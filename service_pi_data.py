#!/usr/bin/env python
# -*- coding: utf_8 -
from parse_json import parseJSON
from config import piServer
def getData(collection):
	print collection
	if(collection["way"]=="sqlite"):
		print "sqlite"
		data=[["2018/10/15 4:11:14","90.64627"],
		["2018/10/15 5:11:14","70.64091"],
		["2018/10/15 6:11:14","45.106"],
		["2018/10/15 7:11:14","20.88336"],
		["2018/10/15 8:11:14","4.46897"],
		["2018/10/15 9:11:14","0.2826293"],
		["2018/10/15 10:11:14","9.356181"],
		["2018/10/15 11:11:14","29.35829"],
		["2018/10/15 12:11:14","54.89384"],
		["2018/10/15 13:11:14","79.11716"],
		["2018/10/15 14:11:14","95.52732"],
		["2018/10/15 15:11:14","99.73225"],
		["2018/10/15 16:11:14","90.64278"],
		]
		data2=[["2018/10/15 4:11:14","90.64627"],
		["2018/10/15 5:11:14","70.64091"],
		["2018/10/15 6:11:14","45.106"],
		["2018/10/15 7:11:14","20.88336"],
		["2018/10/15 12:11:14","54.89384"],
		["2018/10/15 13:11:14","79.11716"],
		["2018/10/15 14:11:14","95.52732"],
		["2018/10/15 15:11:14","99.73225"],
		["2018/10/15 16:11:14","90.64278"],
		]
		data3=[["2018/10/15 4:11:14","90.64627"],
		["2018/10/15 5:11:14","70.64091"],
		["2018/10/15 6:11:14","45.106"],
		["2018/10/15 14:11:14","95.52732"],
		["2018/10/15 15:11:14","99.73225"],
		["2018/10/15 16:11:14","90.64278"],
		]
		if collection["tag"] == "test":
			data = parseJSON(str(collection['fields']),data)
		elif collection["tag"] == "test2":
			data = parseJSON(str(collection['fields']),data2)
		else:
			data = parseJSON(str(collection['fields']),data3)
		return {"data":data,"success":True}
	else:
		import sys  
		import clr
		sys.path.append(r'C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0')    
		clr.AddReference('OSIsoft.AFSDK')
		from OSIsoft.AF import *
		from OSIsoft.AF.PI import *
		from OSIsoft.AF.Asset import *
		from OSIsoft.AF.Data import *
		from OSIsoft.AF.Time import *
		from OSIsoft.AF.UnitsOfMeasure import *
		piServers = PIServers()
		if not collection["ip"]:
			server = piServers.DefaultPIServer
		elif piServer.has_key(collection["ip"]):
			server = piServer[collection["ip"]]
		else:
			server = piServers.get_Item(collection["ip"])
			piServer[collection["ip"]]=server
		pt = PIPoint.FindPIPoint(server,collection["tag"])  
		timerange = AFTimeRange(collection["time_range_start"], collection["time_range_end"])
		span = AFTimeSpan.Parse(collection["AFTimeSpan_Parse"])  
		interpolated = pt.InterpolatedValues(timerange, span, "", False)
		data = []
		for event in interpolated:
			data.append([str(event.Timestamp.LocalTime),str(event.Value)])
			#print('{0} value: {1}'.format(event.Timestamp.LocalTime, event.Value)) 
		data = parseJSON(str(collection['fields']),data)
		return {"data":data,"success":True}
		print ""