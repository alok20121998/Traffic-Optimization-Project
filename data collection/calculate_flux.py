import cv2
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

class Intersection:
    def __init__(self, intersction_id, roadsIn, roadsOut, timeStamps):
        self.id = intersection_id
        self.roadsOut = roadsOut
        self.roadsIn  roadsIn
        self.timeStamps = timeStamps
        self.flux = {}
        self.consideredLen = 50

    def getFlux(self):
        for timeStamp in self.timeStamps:
            flux = {}
            carsOut = 0
            for road in roadsOut:
                carsOut1 = road.getDensityMoving(timeStamp)*self.consideredLen*road.getLanes()
                carsOut+=carsOut1
            for road in roadsOut:
                carsOut1 = road.getDensityMoving(timeStamp)*self.consideredLen*road.getLanes()
                self.flux[road] = carsOut1/carsOut
            self.flux[timeStamp] = flux

class Road:
    def __init__(self, road_id,  lanes, travelSpeedsMoving):
        self.id = road_id
        self.lanes = lanes
        self.lut = np.ndarray(256, dtype = np.float32)
        self.densityMoving = {}
        self.getDensity(self.densityMoving, travelSpeedsMoving)

    def getDensity(self, density, travelSpeeds):
        for timeStamp in travelSpeeds:
            density[timeStamp] = travelSpeeds[timeStamp]

    def getDensityMoving(self, timeStamp):
        return self.densityMoving[timeStamp]

    def getLanes(self):
        return self.lanes

def getFlow():
    df = pd.read_csv('Travel_speeds.csv')
    grouped = df.groupby('Road_id')
    roads = []
    for name, group in grouped:
        travelSpeedsMoving = {}
        for i in group.index:
            travelSpeedsMoving[group[Timestamp][i]] = group[Speed][i]
        roads[name] = Road(name, group[lanes][0], travelSpeedsMoving)
    grouped = df.groupby('Timestamp')
    timeStamps = []
    for name, group in grouped:
        timestamps.append(name)
    df = pd.read_csv('Intersections_in.csv')
    intersections_in = {}
    for i in df.index:
        if df[Intersection_ID][i] not in intersections_in:
            intersections_in[df[Intersection_ID][i]] = [df[Roads_in][i]]
        else:
            intersections_in[df[Intersection_ID][i]].append(df[Roads_in][i])
    df = pd.read_csv('Intersections_out.csv')
    intersections_out = {}
    for i in df.index:
        if df[Intersection_ID][i] not in intersections_out:
            intersections_out[df[Intersection_ID][i]] = [df[Roads_in][i]]
        else:
            intersections_out[df[Intersection_ID][i]].append(df[Roads_in][i])
    intersections = []
    for intersection in intersections_in:
        intersection.append(Intersection(intersection, intersections_in[intersection], intersections_out[intersection]))

getFlow()
