import sys
from math import sqrt
import re
import time

pointRE=re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")
def merge(left, right, v):
	result = []
	i, j = 0, 0
	while (len(result) < len(left) + len(right)):
		if left[i][v] < right[j][v]:
			result.append(left[i])
			i+= 1
		else:
			result.append(right[j])
			j+= 1
		if i == len(left) or j == len(right):
			result.extend(left[i:] or right[j:])
			break
	return result

def mergeSort(points, v):
    if len(points) < 2:
        return points

    m = int(len(points)/2)
    left = mergeSort(points[:m], 0)
    right = mergeSort(points[m:], 0)
    return merge(left, right, v)

def dist(p1, p2):
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

def nearest_neighbor_recursion(points):
    min_distance=0
    num = len(points)

    if num <= 3:
        return brute_force_nearest_neighbor(points)
    else:
        m = int(num/2)          #middle index
        left = points[:m]       #left half of points
        right = points[m:]      #right half of points

        med = right[0]

        ld  = nearest_neighbor_recursion(left)
        rd  = nearest_neighbor_recursion(right)
        if ld <= rd:
            min_distance = ld
        else:
            min_distance = rd

        mid = []
        ysort = mergeSort(points, 1)

        for p in ysort:
                if abs(p[0] - med[0]) < min_distance:
                        mid.append(p)

        size = len(mid)
        if size > 1:
                for i in range(size - 1):
                        for j in range(i+1, min(i+8, size)):
                                if dist(mid[i],mid[j]) < min_distance:
                                        min_distance = dist(mid[i], mid[j])
    return min_distance

#Run the divide-and-conquor nearest neighbor
def nearest_neighbor(points):
    points = mergeSort(points, 0)
    return nearest_neighbor_recursion(points)

#Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    start_time = time.clock()
    min_distance=-1
    for i in range (0, len(points) - 1):
        for j in range (i+1, len(points)):
            d = dist(points[i], points[j])
            if (min_distance == -1) or (min_distance > d):
                min_distance = d
    print("--- %s seconds ---" % (time.clock() - start_time))
    return min_distance

def read_file(filename):
    points=[]
    # File format
    # x1 y1
    # x2 y2
    # ...
    in_file=open(filename,'r')
    for line in in_file.readlines():
        line = line.strip()
        point_match=pointRE.match(line)
        if point_match:
            x = float(point_match.group(1))
            y = float(point_match.group(2))
            points.append((x,y))
    return points

def main(filename,algorithm):
    algorithm=algorithm[0:]
    points=read_file(filename)
    if algorithm =='dc':
        print("Divide and Conquer: ", nearest_neighbor(points))
    if algorithm == 'bf':
        print("Brute Force: ", brute_force_nearest_neighbor(points))
    if algorithm == 'both':
        print("Divide and Conquer: ", nearest_neighbor(points))
        print("Brute Force: ", brute_force_nearest_neighbor(points))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python nearest_neighbor.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python nearest_neighbor.py -<dc|bf|both> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
