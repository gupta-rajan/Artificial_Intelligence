import numpy as np
# import matplotlib.pyplot as plt
import time
import random
import sys

class Coordinates:
    def __init__(self,x,y,id):
        self.x = float(x)
        self.y = float(y)
        self.id = id

    def __repr__(self):
        return "Point"+str(self.id)+":("+str(self.x)+","+str(self.y)+")"


class TSP:
    def getTotalCost(route,distance):
        cost = 0
        for i in range(len(route)-1):
            # print(distance[route[i]][route[i+1]])
            cost += float(distance[route[i]][route[i+1]])
        return cost+float(distance[route[0]][route[-1]])

    def getNewNeighbor1(route):
        k = route.copy()
        p,q = np.random.randint(0,len(k),size =2)
        temp = k[p]
        k[p] = k[q]
        k[q] = temp
        return k

    def sigmoidFunction(delta_E,T):
        return 1/(1+np.exp(min(delta_E/T,709)))
    def exponentialFunction(delta_E,T):
        return np.exp(-delta_E/T)

#greedy approach
def greedy(coords,n,distance):
    # i_node = []
    # min_dist = float("inf")
    # for i in range(n):
    #     for j in range(len(distance[i])):
    #         if float(distance[i][j])<min_dist and [i,j] != i_node and [j,i]!= i_node and i!=j:
    #             i_node = [i,j]
    #             min_dist = float(distance[i][j])
    # init_node = random.choice(i_node)

    init_node = np.random.randint(0,n)
    min_dist = float("inf")
    route = []
    route.append(init_node)

    for i in range(n-1):
        mn = float("inf")
        new_node = -1
        for j in range(len(distance[init_node])):
            if float(distance[init_node][j])<mn and j not in route:
                mn = float(distance[init_node][j])
                new_node = j
        route.append(new_node)
        init_node = new_node
    
    return route

#Simulated annealing Algorithm
def Simulatated_annealing(route,distance,N_iterations,T,factor):
    best_cost = float("inf")
    curr_cost = TSP.getTotalCost(route,distance)
    curr_path = route
    for i in range(N_iterations):
        T = T*factor
        new_path = TSP.getNewNeighbor1(curr_path)
        new_cost = TSP.getTotalCost(new_path,distance)

        if new_cost<curr_cost:
            curr_cost = new_cost
            curr_path = new_path

            if new_cost<best_cost:
                best_cost = new_cost
                best_path = new_path
        else:
            delta_E = new_cost - curr_cost
            P = TSP.sigmoidFunction(delta_E,T)
            if np.random.rand() <= P:
                curr_cost = new_cost
                curr_path = new_path

    return best_cost,best_path

if __name__ == "__main__":
    f = open(str(sys.argv[1]),"r")
    euc = f.readline()
    number_cities = int(f.readline())
    # print(number_cities)

    coords = []
    dist = []
    id = 0
    for p in f:
        coords.append(Coordinates(*p[:-1].split(),id))
        id +=1
        if id == number_cities:
            break

    for p in f:
        dist.append(p[:-1].split())

    # route = np.arange(number_cities)
    # np.random.shuffle(route)
    # print(route)
    # print(getTotalCost(route,dist))

    # Plot
    # print(coords[0].x)
    # cx = [coords[i].x for i in range(number_cities)]
    # cy = [coords[i].y for i in range(number_cities)]
    # plt.plot(cx,cy)
    # plt.show()

    stamp_0 = time.time()
    route = greedy(coords,number_cities,dist)
    # print(TSP.getTotalCost(route,dist))
    cost ,path = Simulatated_annealing(route,dist,100000,10,0.995)
    stamp_1 = time.time()
    # print("The given coordinates are :",coords,"\n")   
    print("The best possible route is :",path)
    print("The minimum cost for the route is :",cost)
    print("Time taken is :",stamp_1-stamp_0)