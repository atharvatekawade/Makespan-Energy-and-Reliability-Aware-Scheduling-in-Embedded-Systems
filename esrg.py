import numpy as np
import math
import config, utils

def esrg(R, l = []):
    if(l == []):
        l, _ = utils.urv()
    
    rels = []
    alloc = []
    freq = []

    for i in range(len(l)):
        rels.append(1)
        alloc.append(-1)
        freq.append(1)

    for i in range(len(l)):
        r_goal = (R**(1 + (i+1)/len(l)))/(np.prod(rels) * R)
        # print("Rel goal:",r_goal)
        emin = float('inf')
        f1 = -1
        pr1 = -1
        dmin = float('inf')
        f2 = -1
        pr2 = -1
        for pr in range(len(config.times)):
            fr = np.arange(config.F_MIN[pr], config.F[pr], 0.0001)
            for f in fr:
                lf = config.L[pr]*10**(config.D[pr]*(1-f)/(1-config.F_MIN[pr]))
                r = math.exp(-lf*config.times[pr][l[i]]/f)
                e = (config.PS[pr] + config.C[pr]*(f**config.A[pr]))*config.times[pr][l[i]]/f
                if(r >= r_goal and e < emin):
                    emin = e
                    f1 = f
                    pr1 = pr
                
                elif(r < r_goal and (r_goal-r) < dmin):
                    dmin = r_goal - r
                    f2 = f
                    pr2 = pr


        if(pr1 != -1): 
            freq[l[i]] = f1   
            alloc[l[i]] = pr1           
        
        else:
            freq[l[i]] = f2  
            alloc[l[i]] = pr2          
        
        lf = config.L[alloc[l[i]]]*10**(config.D[alloc[l[i]]]*(1-freq[l[i]])/(1-config.F_MIN[alloc[l[i]]]))
        r = math.exp(-lf*config.times[alloc[l[i]]][l[i]]/freq[l[i]])
        rels[l[i]] = r
    
    return alloc, freq