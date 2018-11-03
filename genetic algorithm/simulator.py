import requests
import json
import time

class Simulator:
    def __init__(self, stepDuration, areaOptimized, areaCalculated):
        self.stepDuration = stepDuration
        self.areaOptimized = areaOptimized
        self.areaCalculated = areaCalculated

    def requestStats(self, data, username = 'pgora', password = 'Ghzf8ftb', address = 'http://13.81.247.156:25041/compute'):
        headers = {'Content-type': 'application/json',}
        data = '{"settings": "' + str(data) + '"}'
        response = ''
        result = 0
        while True:
            try:
                response = requests.post(address, headers=headers, data=data)
                text = str(response.content,"utf-8") if isinstance(response.content, bytes) else response.content
                result = int(json.loads(text)['score']) 
                print(' result: ', result, ' data: ',data)
                break
            except Exception as e:
                if(response.status_code==201):
                    text = str(response.content,"utf-8") if isinstance(response.content, bytes) else response.content
                    result = int(json.loads(text)['score']) 
                    print(' result: ', result, ' data: ',data)
                    return result;
                print(': There were sme problems!!!!!!!!!',response, response.content)
        return result


    def getFitness1(self, timings):
        fitness = 0
        for timing in timings:
            start = time.time()
            result = self.requestStats(timing.tolist())
            end = time.time()
            print(end-start)
            fitness+=result
            print(fitness)
        return fitness

    def getFitness2(self, timings):
        fitness = 0
        for timing in timings:
            result = self.requestStats(timing.tolist())
            fitness+=result
            print(fitness)
        return fitness

    def getFitness3(self, timings, densities):
        fitness = 0
        for timing in timings:
            result = self.requestStats(timing.tolist())
            fitness+=result
            print(fitness)
        return fitness
