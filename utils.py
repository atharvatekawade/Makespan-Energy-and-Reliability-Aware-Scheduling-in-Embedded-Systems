import random
import math
import config

def random_proc():
    alloc = []
    for i in range(len(config.graph)):
        alloc.append(random.randint(0, len(config.times)-1))
    
    return alloc

def urv():
    x = [[i, 0] for i in range(len(config.graph))]

    for i in range(len(config.graph)-1, -1, -1):
        mt = 0
        for j in range(len(config.graph)):
            if(config.graph[i][j] > 0):
                mt = max(mt, x[j][1]+config.graph[i][j])
        
        rnk = 0

        for j in range(len(config.times)):
            rnk += config.times[j][i]
        
        x[i][1] = rnk/len(config.times) + mt

    x.sort(key=lambda x: x[1], reverse= True) 
    return [x[i][0] for i in range(len(x))], [x[i][1] for i in range(len(x))]

def simulate(alloc, freq = [], l = []):
    r = 1
    e = 0

    if(l == []):
        l, _ = urv()

    
    if(freq == []):
        for _ in range(len(config.graph)):
            freq.append(1)
    
    for i in range(len(l)):
        for j in range(len(l)):
            if(config.graph[l[i]][l[j]] > 0 and i >= j):
                print("Wrong config.graph levels")
                quit()

    starts = []
    fins = []
    avail = []

    for i in range(len(config.times)):
        avail.append(0)

    for i in range(len(l)):
        starts.append(0)
        fins.append(0)

    for i in range(len(l)):
        pr = alloc[l[i]]
        s = avail[pr]
        for j in range(len(config.graph)):
            if(config.graph[j][l[i]] > 0):
                comm = config.graph[j][l[i]]
                if(pr == alloc[j]):
                    comm = 0

                s = max(s, fins[j]+comm)

        f = s + config.times[pr][l[i]]/freq[l[i]]
        

        starts[l[i]] = s
        fins[l[i]] = f  
        avail[pr] = fins[l[i]]

        e = e + (config.PS[pr] + config.C[pr]*(freq[l[i]]**config.A[pr]))*config.times[pr][l[i]]/freq[l[i]]

        lf = config.L[pr]*10**(config.D[pr]*(1-freq[l[i]])/(1-config.F_MIN[pr]))
        r = r * math.exp(-lf*config.times[pr][l[i]]/freq[l[i]])

    
    return max(fins), r, e


def soea1(alloc, R):
    y1 = []
    y2 = []

    for pr in range(len(config.times)):
        num = config.C[pr]*(config.A[pr]-1)*(config.F_MIN[pr]**(config.A[pr]-1)) - config.PS[pr]/config.F_MIN[pr]
        lf = config.L[pr]*10**(config.D[pr]*(1-config.F_MIN[pr])/(1-config.F_MIN[pr]))
        den = config.D[pr]*math.log(10)/(1-config.F_MIN[pr]) + 1/config.F_MIN[pr]
        y1.append(num/(R*lf*den))

        num = config.C[pr]*(config.A[pr]-1)*(config.F[pr]**(config.A[pr]-1)) - config.PS[pr]/config.F[pr]
        lf = config.L[pr]*(10**(config.D[pr]*(1-config.F[pr])/(1-config.F_MIN[pr])))
        den = config.D[pr]*math.log(10)/(1-config.F_MIN[pr]) + 1/config.F[pr]
        y2.append(num/(lf*den))

    lb = min(y1)
    ub = max(y2)
    freq = []

    freq = []
    for i in range(len(config.graph)):
        freq.append(1)

    while(ub - lb > config.epsilon):
        mid = (ub+lb)/2

        for pr in range(len(config.times)):
            flb = config.F_MIN[pr]
            fub = config.F[pr]
            f = (flb+fub)/2
            while(fub - flb > config.epsilon):
                num = config.C[pr]*(config.A[pr]-1)*(f**(config.A[pr]-1)) - config.PS[pr]/f
                lf = config.L[pr]*(10**(config.D[pr]*(1-f)/(1-config.F_MIN[pr])))
                den = config.D[pr]*math.log(10)/(1-config.F_MIN[pr]) + 1/f
                y = num/(R*lf*den)

                if(y < mid):
                    flb = f
                else:
                    fub = f
                f = (flb+fub)/2

            for i in range(len(config.graph)):
                if(alloc[i] == pr):
                    freq[i] = f   

        _, r, _ = simulate(alloc, freq=freq)

        if(r < R):
            lb = mid
        else:
            ub = mid
    
    return freq


def heft(l = []):
    if(l == []):
        l, _ = urv()
    
    for i in range(len(config.graph)):
        for j in range(len(config.graph)):
            if(config.graph[i][j] > 0 and l.index(i) >= l.index(j)):
                print("Wrong config.graph levels")
                quit()

    fins = []
    alloc = []
    avail = []

    for i in range(len(config.times)):
        avail.append(0)

    for i in range(len(l)):
        fins.append(0)
        alloc.append(-1)

    for i in range(len(l)):
        fmin = float('inf')
        for j in range(len(config.times)):
            s = avail[j]
            for k in range(len(config.graph)):
                if(config.graph[k][l[i]] > 0):
                    comm = config.graph[k][l[i]]
                    if(j == alloc[k]):
                        comm = 0

                    s = max(s, fins[k]+comm)

            f = s + config.times[j][l[i]]

            if(f < fmin):
                fmin = f
                alloc[l[i]] = j

        fins[l[i]] = fmin  
        avail[alloc[l[i]]] = fins[l[i]]

    return alloc, max(fins)


def lec(l = []):
    if(l == []):
        l, _ = urv()
    
    for i in range(len(l)):
        for j in range(len(l)):
            if(config.graph[l[i]][l[j]] > 0 and i >= j):
                print("Wrong config.graph levels")
                quit()

    starts = []
    fins = []
    avail = []
    alloc = []

    for i in range(len(config.times)):
        avail.append(0)

    for i in range(len(l)):
        starts.append(0)
        fins.append(0)
        alloc.append(-1)

    for i in range(len(l)):
        emin = float('inf')
        for j in range(len(config.times)):
            s = avail[j]
            for k in range(len(config.graph)):
                if(config.graph[k][l[i]] > 0):
                    comm = config.graph[k][l[i]]
                    if(j == alloc[k]):
                        comm = 0

                    s = max(s, fins[k]+comm)

            f = s + config.times[j][l[i]]
            e1 = (config.PS[j] + config.C[j]*(config.F[j]**config.A[j]))*config.times[j][l[i]]/config.F[j]

            if(e1 < emin):
                emin = e1
                alloc[l[i]] = j
                fins[l[i]] = f
 
        avail[alloc[l[i]]] = fins[l[i]]

    return alloc, max(fins)

def mr(l = []):
    if(l == []):
        l, _ = urv()
    
    for i in range(len(l)):
        for j in range(len(l)):
            if(config.graph[l[i]][l[j]] > 0 and i >= j):
                print("Wrong config.graph levels")
                quit()

    starts = []
    fins = []
    avail = []
    alloc = []

    for i in range(len(config.times)):
        avail.append(0)

    for i in range(len(l)):
        starts.append(0)
        fins.append(0)
        alloc.append(-1)

    for i in range(len(l)):
        rmax = 0
        for j in range(len(config.times)):
            s = avail[j]
            for k in range(len(config.graph)):
                if(config.graph[k][l[i]] > 0):
                    comm = config.graph[k][l[i]]
                    if(j == alloc[k]):
                        comm = 0

                    s = max(s, fins[k]+comm)

            f = s + config.times[j][l[i]]
            lf = config.L[j]*10**(config.D[j]*(1-config.F[j])/(1-config.F_MIN[j]))
            r1 = math.exp(-lf*config.times[j][l[i]]/config.F[j])

            if(r1 > rmax):
                rmax = r1
                alloc[l[i]] = j
                fins[l[i]] = f
 
        avail[alloc[l[i]]] = fins[l[i]]

    return alloc, max(fins)

