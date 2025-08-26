#!/usr/bin/python3

import csv
import sys
import math
#from tabulate import tabulate

from dataclasses import dataclass

@dataclass
class Tarea:
    c: int
    t: int
    d: int

def tests(tareas, streal):
    print("----------------------------------------")
    print()

    print("[+] STR: ("+ "),(".join(streal)+ ")")
    print(f"Hiperperiodo: {hiperperiodo(tareas)}")
    print(f"Factor de utilización: {round(fu(tareas),2)}")
    print(f"Cota de Liu para RM/DM: {round(liu_rm_dm(tareas),2)}")
    print(f"Cota de Bini para RM: {round(bini(tareas),2)}")
    print("WCRT: (R, Iteraciones, Techos calculados)")
    print(f"Joshep: {joseph(tareas)}")
    #print(tabulate(zip(joseph(tareas),rta(tareas)), headers= ["R","Iteraciones","Techos","R","Iteraciones","Techos"]))
    print(f"RTA: {rta(tareas)}")
    print(f"Primera ranura libre: {ranuras_vacias(tareas)}")

    print()

def hiperperiodo(tareas):
    last = 1
    for tarea in tareas:
        last =  math.lcm(tarea.t,last)
    return last

def fu(tareas):
    result = 0
    for tarea in tareas:
        result = result + tarea.c/tarea.t 
    return result

def liu_rm_dm(tareas):
    n = len(tareas)
    return n*((2**(1/n))-1)

def bini(tareas):
    result = 1
    for tarea in tareas:
        result = result* (tarea.c/tarea.t +1)
    return result

def joseph(tareas):
    results = []
    index = 0
    for tarea in tareas:
        iteraciones=0
        techos=0
        t=0
        anteriores = tareas[0:index] 
        result = 0
        while True:
            iteraciones +=1
            sumatoria = 0
            for ant in anteriores:
                sumatoria = sumatoria + (ant.c * math.ceil(t/ant.t))
                techos +=1
            result = tarea.c + sumatoria
            if result == t:
                index+=1
                break
            t=result

        results.append((result,iteraciones,techos))
    return results

def rta(tareas):
    results = []
    index = 0
    for tarea in tareas:
        iteraciones=0
        techos=0
        t = (results[-1][0] + tarea.c) if results else tarea.c
        anteriores = tareas[0:index] 
        result = 0
        while True:
            iteraciones += 1
            sumatoria = 0
            for ant in anteriores:
                sumatoria = sumatoria + (ant.c * math.ceil(t/ant.t))
                techos += 1
            result = tarea.c + sumatoria
            if result == t:
                index+=1
                break
            t=result

        results.append((result,iteraciones,techos))
    return results

def ranuras_vacias(tareas):
    results = []
    index = 1
    for tarea in tareas:
        t = (results[-1] - 1) if results else tarea.c
        anteriores = tareas[0:index] 
        result = 0
        while True:
            sumatoria = 0
            for ant in anteriores:
                sumatoria = sumatoria + (ant.c * math.ceil(t/ant.t))
            result = 1 + sumatoria
            if result == t:
                index+=1
                break
            t=result

        results.append(result)
    return results



with open('input.csv', newline="") as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for row in reader:
        tareas = []
        for item in row:
            c, t, d = map(int, item.split(","))
            tareas.append(Tarea(c, t, d))
        tests(tareas,row)


