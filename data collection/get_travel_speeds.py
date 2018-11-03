import requests
import time
import pandas as pd

def getTravelSpeeds(points):
    URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    key = "hiAG9GwBH92YXjGDPQaFTvS3zjJr9ihr"
    speeds = {}
    for point in points:
        parameters = {'key':key, 'point':point}
        r = requests.get(url = URL, params = parameters)
        data = r.json()
        speeds[point] = data["flowSegmentData"]["currentSpeed"]
    return speeds

def getTravelSpeedsOverTime(points):
    startTime = time.time()
    speedsOverTime = {}
    i = 0
    while(i<2):
        speedsOverInterval = []
        t1 = time.time()
        while(time.time()<t1+15):
            speedsOverInterval.append(getTravelSpeeds(points))
        t2 = time.time()
        averageSpeeds = {}
        for point in points:
            speed = 0
            for speeds in speedsOverInterval:
                speed+=speeds[point]
            speed/=len(speedsOverInterval)
            averageSpeeds[point] = speed
        speedsOverTime[(t1+t2)//2] = averageSpeeds
        i+=1
    return speedsOverTime

def addSpeedData():
    df = pd.read_csv("road_coordinates.csv")
    lanes_and_lengths = df.set_index('Coordinates').T.to_dict('list')
    df2 = pd.DataFrame(columns = ['Timestamp', 'Speed', 'Coordinates', 'Lanes', 'Length', 'Road_id'])
    points = list(df.loc[:, 'Coordinates'])
    travelSpeedsOverTime = getTravelSpeedsOverTime(points)
    index = 0
    for timeStamp in travelSpeedsOverTime:
        for point in travelSpeedsOverTime[timeStamp]:
            df2.loc[index] = [timeStamp, travelSpeedsOverTime[timeStamp][point], point, lanes_and_lengths[point][1], lanes_and_lengths[point][2], points.index(point)]
            index+=1
    df2.to_csv("Travel_speeds.csv", sep = '\t')
    print(df2)
addSpeedData()
