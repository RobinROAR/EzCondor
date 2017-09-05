#!/usr/bin/env python
# -*-coding:utf-8 -*-
#Robin
#04.21 2017
import random

network = {'A':['B','D','E'],'B':['D','A','E'],'C':['B','F'],'D':['A','B'],'E':['A','F'],'F':['C','E']}


def diffusion(network,source,p):
    visited = {}
    #create a list to store influenced node
    influenced = {}
    for node in network:
        visited[node] = False
        influenced[node] = False

    visited[source] = True
    queue = [source]
    influenced[source] = True

    while queue!=[] :
        now = queue.pop(0)
        #只有被influcenced的才扩散
        if influenced[now] == True:
            for neighbor in network[now]:
                if visited[neighbor] == False:
                    visited[neighbor] = True
                    #有p的概率传播成功
                    if random.random()<= p:
                        influenced[neighbor] = True
                    queue.append(neighbor)
    #统计结果
    result = []
    for key,value in influenced.items():
        if value == True:
            result.append(key)

    return len(result)



print diffusion(network,'A',0.15)