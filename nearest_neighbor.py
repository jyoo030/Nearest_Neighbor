import sys
from math import sqrt
import re
import time

pointRE=re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")


def dist(p1, p2):
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

def nearest_neighbor_recursion(points):
    min_distance=0
    length = len(points)

    if length <= 3:
        return brute_force_nearest_neighbor(points)
    else:
        c = int(length/2)
        left = points[:c]
        right = points[c:]

        med = right[0]

        ld  = nearest_neighbor_recursion(left)
        rd  = nearest_neighbor_recursion(right)
        if ld <= rd:
            min_distance = ld
        else:
            min_distance = rd
        mid = []
        sortsort = sorted(points, key=lambda x:x[1])
        for k in sortsort:
                if abs(k[0] - med[0]) < min_distance:
                        mid.append(k)
        size = len(mid)
        if size > 1:
                for i in range(size - 1):
                        for j in range(i+1, min(i+8, size)):
                                if dist(mid[i],mid[j]) < min_distance:
                                        min_distance = dist(mid[i], mid[j])
    return min_distance

# Run the divide-and-conquor nearest neighbor
def nearest_neighbor(points):
    points = sorted(points, key=lambda x:x[0])
    return nearest_neighbor_recursion(points)

#Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    min_distance=-1
    for i in range (0, len(points) - 1):
        for j in range (i+1, len(points)):
            d = dist(points[i], points[j])
            if (min_distance == -1) or (min_distance > d):
                min_distance = d
    return min_distance

def read_file(filename):
    points=[]
    in_file=open(filename,'r')
    for line in in_file.readlines():
        line = line.strip()
        point_match=pointRE.match(line)
        if point_match:
            x = float(point_match.group(1))
            y = float(point_match.group(2))
            points.append((x,y))
    return points

def main(filename):
    points=read_file(filename)
    average = 0
    start_time = time.clock()
    distance = nearest_neighbor(points)
    # distance = brute_force_nearest_neighbor(points)
    tm = (time.clock() - start_time)
    print("--- %s seconds ---" % tm)
    text_write = open(filename + "_distance.txt", "w")
    hello = str(distance)
    text_write.write(hello)
    text_write.close()

main(sys.argv[1])
