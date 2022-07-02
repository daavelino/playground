import sys
from pprint import pprint


filename = sys.argv[1]

with open(filename, "r") as f:
    result = dict()
    data = f.readlines()
    
    for i in data:
        tmp = i.split()
        if tmp[1] not in result.keys():
            result[tmp[1]] = 1
        else:
            result[tmp[1]] += 1


    pprint(result)

