import pandas as pd
from utils import Euclidean
import ast

map = pd.read_excel("map350_040122_X.xlsx")
nodes = []
d = dict()
for i in range(len(map.index)):
    for j in range(len(map.columns)):
        temp = map.iloc[i][j].split(",")
        if temp[0] == 'x':
            if map.iloc[i - 1][j].split(",")[0] != "q":
                nodes.append([i - 1, j, map.iloc[i - 1][j].split(",")])
            if map.iloc[i + 1][j].split(",")[0] != "q":
                nodes.append([i + 1, j, map.iloc[i + 1][j].split(",")])
            if map.iloc[i][j - 1].split(",")[0] != "q":
                nodes.append([i, j - 1, map.iloc[i][j - 1].split(",")])
            if map.iloc[i][j + 1].split(",")[0] != "q":
                nodes.append([i, j + 1, map.iloc[i][j + 1].split(",")])
        if len(temp) >= 2:
            nodes.append([i, j, temp])

"""gen undirected graph"""
for node in nodes:
    minXleftOfNode = 100000
    minXrightOfNode = 100000
    minYupOfNode = 100000
    minYdownOfNode = 100000
    eNodes = []
    for node2 in nodes:
        temp = Euclidean(node[0], node[1], node2[0], node2[1])
        if node[0] == node2[0] and node[1] == node2[1]:
            continue
        if node[0] == node2[0] and (node[1] - node2[1]) < 0:
            if temp < minYupOfNode:
                minYupOfNode = temp
        if node[0] == node2[0] and (node[1] - node2[1]) > 0:
            if temp < minYdownOfNode:
                minYdownOfNode = temp

        if node[1] == node2[1] and node[0] - node2[0] < 0:
            if temp < minXrightOfNode:
                minXrightOfNode = temp
        if node[1] == node2[1] and node[0] - node2[0] > 0:
            if temp < minXleftOfNode:
                minXleftOfNode = temp

    for node3 in nodes:
        temp = Euclidean(node[0], node[1], node3[0], node3[1])
        if node[0] == node3[0] and temp == minYupOfNode and node[1] - node3[1] < 0:
            eNodes.append(node3)
        if node[0] == node3[0] and temp == minYdownOfNode and node[1] - node3[1] > 0:
            eNodes.append(node3)
        if node[1] == node3[1] and temp == minXleftOfNode and node[0] - node3[0] > 0:
            eNodes.append(node3)
        if node[1] == node3[1] and temp == minXrightOfNode and node[0] - node3[0] < 0:
            eNodes.append(node3)
    d[str(node)] = eNodes

vertexes = dict()
"""gen directed graph"""
for node1 in d:
    node1_change = ast.literal_eval(node1)
    list_node = []
    for node2 in d[node1]:
        dir = None
        temp = set(node2[2]).intersection(set(node1_change[2]))
        if node1_change[0] == node2[0]:
            if node1_change[1] - node2[1] > 0:
                dir = 'l'
            if node1_change[1] - node2[1] < 0:
                dir = 'r'
        if node1_change[1] == node2[1]:
            if node1_change[0] - node2[0] < 0:
                dir = 'd'
            if node1_change[0] - node2[0] > 0:
                dir = 'u'
        if dir in temp:
            list_node.append([node2[1], node2[0],Euclidean(node1_change[1], node1_change[0], node2[1], node2[0])])

    vertexes[str([node1_change[1], node1_change[0]])] = list_node

for i in vertexes:
    print(i + " " + str(vertexes[i]))

