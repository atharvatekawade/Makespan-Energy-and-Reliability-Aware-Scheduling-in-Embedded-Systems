import random

def init(pr, n):
    global graph
    global times

    global PS
    global C
    global F
    global F_MIN
    global A
    global L
    global D

    global t1
    global t2
    global ods_results
    global ods_alloc
    global my_results
    global my_alloc
    global epsilon

    graph = []
    times = []

    PS = []
    C = []
    F = []
    F_MIN = []
    A = []
    L = []
    D = []

    t1 = 10
    t2 = 100
    ods_results = []
    ods_alloc = []
    my_results = []
    my_alloc = []
    epsilon = 10**(-5)
    
    v = (2+n)*2**n - 1

    for i in range(v):
        graph.append([])
        for _ in range(v):
            graph[i].append(0)

    curr_level = [0]
    next_level = []

    for _ in range(n):
        next_level = []
        for i in range(len(curr_level)):
            graph[curr_level[i]][2*curr_level[i]+1] = random.randint(t1, t2)
            next_level.append(2*curr_level[i]+1)

            graph[curr_level[i]][2*curr_level[i]+2] = random.randint(t1, t2)
            next_level.append(2*curr_level[i]+2)
            
        curr_level = next_level[:]
        
    for i in range(n):
        next_level = []
        turn = []
        curr = 0
        ctr = 0
        for j in range(len(curr_level)):
            next_level.append(curr_level[j]+2**n)
            turn.append(curr)
            ctr += 1
            if(ctr == 2**i):
                ctr = 0
                curr = 1 - curr
            
        for j in range(len(curr_level)):
            graph[curr_level[j]][next_level[j]] = random.randint(t1, t2)
            if(turn[j] == 0):
                graph[curr_level[j]][next_level[j]+2**i] = random.randint(t1, t2)
            else:
                graph[curr_level[j]][next_level[j]-2**i] = random.randint(t1, t2)

        curr_level = next_level[:]
    
    for i in range(pr):
        times.append([])
        for _ in range(len(graph)):
            times[i].append(random.randint(t1, t2))
    
    for i in range(len(times)):
        PS.append(random.randint(400, 800)/1000)
        C.append(random.randint(800, 1300)/1000)
        F.append(1)
        F_MIN.append(0.3)
        A.append(random.randint(2700,3000)/1000)
        L.append(random.randint(100, 1000)/10**8)
        D.append(random.randint(1000, 3000)/1000)