import math
import json
from telnetlib import theNULL
import urllib.request as req
from datetime import datetime
from datetime import timedelta

class Vertex:
    def __init__(self, city,lat,long):
        self.id = city
        self.lat=lat
        self.long=long
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0,distance=0):
        self.adjacent[neighbor] = [weight,distance]

    def get_connections(self):
        return self.adjacent.keys()  

    def get_city(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor][0]
    def get_distance(self, neighbor):
        return self.adjacent[neighbor][1]
    
    def cal_distance(self,other):
        lat1=self.lat
        lat2=other.lat
        lon1=self.long
        lon2=other.long
        R = 6371000
        φ1 = lat1 * math.pi/180
        φ2 = lat2 * math.pi/180 
        Δφ = (lat2-lat1) * math.pi/180
        Δλ = (lon2-lon1) * math.pi/180
        a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c*0.000621371192


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node,lat,long):
        if node not in self.vert_dict:
            self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node,lat,long)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm == to:
            return;
        distance=self.vert_dict[frm].cal_distance(self.vert_dict[to])
        fuel_cost=distance*0.40
        cost-=fuel_cost
        cost=-(cost)
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost,distance)

    def get_vertices(self):
        return self.vert_dict.keys()
    
    def printArr(self, dist):
        max_profit=float("inf")
        best_i=""
        paths=[]
        for i in dist:
            if i!="source":
                if dist[i][0]<max_profit or dist[i][0]<0:
                    max_profit=dist[i][0]
                    best_i=i
                    paths.append(dist[best_i][1]+[best_i])
        print(paths)
        return paths

    def BellmanFord(self, src , maxdistance):
        dist = self.vert_dict.copy()
        for key in dist:
            dist[key]=[float("inf"),[],0]
        dist[src] = [0,[],0]
        i=0
        for _ in range(self.num_vertices-1):
            for vertex in g.vert_dict:
                for u in g.vert_dict[vertex].adjacent:
                    w=g.vert_dict[vertex].get_weight(u)
                    d=g.vert_dict[vertex].get_distance(u)
                    u=u.get_city()
                    if dist[vertex][0] != float("Inf") and dist[vertex][0] + w < dist[u][0] and dist[vertex][2] + d <= maxdistance :
                        dist[u][0] = dist[vertex][0] + w
                        dist[u][1] = dist[vertex][1] + [vertex]
                        dist[u][2] = dist[vertex][2] + d
            i+=1
            print(i)
        return dist
    
def cal_maxdistance(initialtime,endtime):
    TIME_MASK="%Y-%m-%d %H:%M:%S"
    time1= datetime.strptime(initialtime, "%Y-%m-%d %H:%M:%S")
    time2= datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")
    duration =time2-time1
    duration_in_s= duration.total_seconds()
    hours = divmod(duration_in_s, 3600)[0]
    distance=hours*55
    return distance

def convert_path_to_json(paths,marketplace,trip_id,trucker):
    load_ids=[]
    for i in range(len(paths)):
        path=paths[(len(paths)-1)-i]
        k=0
        for i in range(len(path)):
            for j in marketplace:
                if j["origin_city"]+j["origin_state"]==path[i] and i+1<len(path):
                    if j["destination_city"]+j["destination_state"]==path[i+1]:
                        if datetime.strptime(j["pickup_date_time"], "%Y-%m-%dT%H:%M:%S.000Z")<datetime.strptime(trucker["max_destination_time"], "%Y-%m-%d %H:%M:%S") and datetime.strptime(j["pickup_date_time"], "%Y-%m-%dT%H:%M:%S.000Z")>datetime.strptime(trucker["start_time"], "%Y-%m-%d %H:%M:%S"):
                            load_ids.append(j["load_id"])
                            break;
        if len(load_ids)>=len(path)-2:
            break;
        else:
            load_ids=[]
    dictionary={"trip_id":trip_id, "load_id":load_ids}
    return dictionary

TRUCK_SPEED= 55
FUEL_COST=0.40
TIME_MASK="%Y-%m-%d %H:%M:%S"
TIME_MASK2="%Y-%m-%dT%H:%M:%S.000Z"

def cal_distance(lat1, lat2, lon2, lon1):
    R = 6371000
    φ1 = lat1 * math.pi/180
    φ2 = lat2 * math.pi/180 
    Δφ = (lat2-lat1) * math.pi/180
    Δλ = (lon2-lon1) * math.pi/180

    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def cal_timetrip(distance):
    return distance/TRUCK_SPEED

def cal_fuelcost(distance):
    return distance*FUEL_COST

def addhour(date1,hour):
    year1=date1[0:4]
    month1=date1[5:7]
    day1=date1[8:10]
    hour1=date1[11:13]
    min1=date1[14:16]
    sec1=date1[17:19]
    ms1=date1[20:23]
    if month1=="02" :
        if ms1!='':
            date_and_time = datetime(int(year1), int(3), int(day1), int(hour1), int(min1), int(sec1),int(ms1))
        else:
            date_and_time = datetime(int(year1), int(3), int(day1), int(hour1), int(min1), int(sec1))
        time_change = timedelta(hours=hour)
        new_time = date_and_time + time_change
        return str(new_time)[:5]+"02"+str(new_time)[8:]
    elif ms1!='':
        date_and_time = datetime(int(year1), int(month1), int(day1), int(hour1), int(min1), int(sec1),int(ms1))
    else:
        date_and_time = datetime(int(year1), int(month1), int(day1), int(hour1), int(min1), int(sec1))
    time_change = timedelta(hours=hour)
    new_time = date_and_time + time_change
    return str(new_time)


def comparedates(date1,date2):
    """if date1 is after date2"""
    year1=date1[0:4]
    month1=date1[5:7]
    day1=date1[8:10]
    hour1=date1[11:13]
    min1=date1[14:16]
    sec1=date1[17:19]
    ms1=date1[20:23]
    year2=date2[0:4]
    month2=date2[5:7]
    day2=date2[8:10]
    hour2=date2[11:13]
    min2=date2[14:16]
    sec2=date2[17:19]
    ms2=date2[20:23]
    if year2<year1:
        return True
    elif month2<month1:
        return True
    elif day2<day1:
        return True
    elif hour2<hour1:
        return True
    elif min2<min1:
        return True
    elif sec2<sec1:
        return True
    elif ms1!='' or ms2!='':
        if ms2<ms1:
            return True
    return False

def remove_candidates(marketplace,trucker):
    """Remove unachievable time deliveries"""
    i=0
    for key in marketplace:
        distance= cal_distance(key["origin_latitude"],key["destination_latitude"],key["origin_longitude"],key["destination_longitude"])
        time= cal_timetrip(distance)
        if comparedates(addhour(trucker['start_time'],time),key['pickup_date_time']):
            del marketplace[i]
        elif comparedates(addhour(key['pickup_date_time'],time),trucker["max_destination_time"]):
            del marketplace[i]
        i+=1
if __name__ == '__main__':

    
    with open('input.json') as url:
        input = json.load(url)


    # print(g.num_vertices)
    list=[]
    for trucker in input:

        g = Graph()

        with req.urlopen("https://codejam.123loadboard.com/data/123Loadboard_CodeJam_2022_dataset.json") as url:
            marketplace = json.loads(url.read().decode())

        for load in marketplace:
            g.add_vertex(load["origin_city"]+load["origin_state"],load["origin_latitude"],load["origin_longitude"])
            g.add_vertex(load["destination_city"]+load["destination_state"],load["destination_latitude"],load["destination_longitude"])
            g.add_edge(load["origin_city"]+load["origin_state"], load["destination_city"]+load["destination_state"], load["amount"]) 

        g.add_vertex("source",trucker["start_latitude"],trucker["start_longitude"])
        for v in g.vert_dict:
            g.add_edge("source",v) 
    
        maxD=cal_maxdistance(trucker["start_time"],trucker["max_destination_time"])
        path=g.printArr(g.BellmanFord("source",maxD))
        dictionary  =convert_path_to_json(path,marketplace,trucker["input_trip_id"],trucker)
        list.append(dictionary)


        
    json_object = json.dumps(list, indent = 4)
  
        # Writing to sample.json
    with open("output_s400.json", "w") as outfile:
        outfile.write(json_object)
