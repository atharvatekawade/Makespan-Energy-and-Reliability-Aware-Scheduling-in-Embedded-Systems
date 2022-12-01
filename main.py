import config, utils, esrg, ods, wanms
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME -p PASSWORD -size 20000
parser.add_argument("-rho", dest = "rho", default = 3, type=int)
parser.add_argument("-itr", dest = "itr", default = 5, type=int)
parser.add_argument("-pr", dest = "pr", default = 16, type=int)
parser.add_argument("-R", dest = "R", default = 0.9, type=float)
parser.add_argument("-smin", dest = "smin", default = 10, type=int)
parser.add_argument("-smax", dest = "smax", default = 10**2, type=int)
parser.add_argument("-ods_start", dest = "ods_start", default = 10, type=float)
parser.add_argument("-ods_end", dest = "ods_end", default = 100, type=float)
parser.add_argument("-ods_step", dest = "ods_step", default = 10, type=float)
parser.add_argument("-wanms_start", dest = "wanms_start", default = 0, type=float)
parser.add_argument("-wanms_end", dest = "wanms_end", default = 1, type=float)
parser.add_argument("-wanms_step", dest = "wanms_step", default = 0.1, type=float)


args = parser.parse_args()

config.t1 = args.smin
config.t2 = args.smax

results = [[0, 0, 0] for _ in range(6)]
rel_constraint = 0

for gen in range(args.itr):
    config.init(args.pr, args.rho)

    print("Running ODS")
    ods.ods(args.ods_start, args.ods_end, args.ods_step)

    print("Running WANMS")
    wanms.my(args.wanms_start, args.wanms_end, args.wanms_step)

    alloc, _ = utils.mr()
    _, max_rel, _ = utils.simulate(alloc)


    fails = [0, 0, 0, 0, 0, 0]
    R = args.R*max_rel
    rel_constraint += R
    print("Constraint:",R)
        
    alloc, _ = utils.heft()
    f1, r1, e1 = utils.simulate(alloc)
    freq = utils.soea1(alloc, R)
    f1, r1, e1 = utils.simulate(alloc, freq=freq)
            
    if(R - r1 >= config.epsilon):
        print("HEFT failed", R, r1)
        fails[0] += 1
        alloc, _ = utils.mr()
        freq = utils.soea1(alloc, R)
        f1, r1, e1 = utils.simulate(alloc, freq=freq)

    print(f"Algo: HEFT+SOEA  No. of vertices: {len(config.graph)} Span: {f1} Rel: {r1} Energy: {e1}")
    results[0][0] += f1
    results[0][1] += r1
    results[0][2] += e1

    alloc, _ = utils.lec()
    f1, r1, e2 = utils.simulate(alloc)
    freq = utils.soea1(alloc, R)
    f1, r1, e2 = utils.simulate(alloc, freq=freq)

    if(R - r1 >= config.epsilon):
        print("LEC failed", R, r1)
        fails[1] += 1
        alloc, _ = utils.mr()
        freq = utils.soea1(alloc, R)
        f1, r1, e2 = utils.simulate(alloc, freq=freq)

    print(f"Algo: LEC+SOEA  No. of vertices: {len(config.graph)} Span: {f1} Rel: {r1} Energy: {e2}")
    results[1][0] += f1
    results[1][1] += r1
    results[1][2] += e2

    alloc, _ = utils.mr()
    f1, r1, e3 = utils.simulate(alloc)
    freq = utils.soea1(alloc, R)
    f1, r1, e3 = utils.simulate(alloc, freq = freq)
    print(f"Algo: MR+SOEA  No. of vertices: {len(config.graph)} Span: {f1} Rel: {r1} Energy: {e3}")

    results[2][0] += f1
    results[2][1] += r1
    results[2][2] += e3

    alloc, freq = esrg.esrg(R)
    f1, r1, e4 = utils.simulate(alloc, freq=freq)
    print(f"Algo: ESRG No. of vertices: {len(config.graph)} Span: {f1} Rel: {r1} Energy: {e4}")

    if(R > r1):
        fails[3] += 1
        alloc, _ = utils.mr()
        freq = utils.soea1(alloc, R)
        f1, r1, e4 = utils.simulate(alloc, freq=freq)

    results[3][0] += f1
    results[3][1] += r1
    results[3][2] += e4

    E = min(e1, e2, e3, e4)

    alloc, f, r, e = ods.ods_output(R, E)
    print(f"Algo: ODS+SOEA No. of vertices: {len(config.graph)} Span: {f} Rel: {r} Energy: {e}")
        

    if(f == float('inf')):
        fails[4] += 1
        alloc, _ = utils.mr()
        freq = utils.soea1(alloc, R)
        f, r, e = utils.simulate(alloc, freq=freq)

    results[4][0] += f
    results[4][1] += r
    results[4][2] += e

    _, f, r, e = wanms.my_output(R, E)
    print(f"Algo: WANMS+SOEA No. of vertices: {len(config.graph)} Span: {f} Rel: {r} Energy: {e}")

    if(f1 == float('inf')):
        fails[5] += 1
        alloc, _ = utils.mr()
        freq = utils.soea1(alloc, R)
        f, r, e = utils.simulate(alloc, freq=freq)

    results[5][0] += f
    results[5][1] += r
    results[5][2] += e

    print("\n")

for i in range(len(results)):
    for j in range(len(results[i])):
        results[i][j] = results[i][j]/args.itr

print(f"Algo: HEFT+SOEA No. of vertices: {len(config.graph)} Span: {results[0][0]} Rel: {results[0][1]} Energy: {results[0][2]} Fails: {fails[0]}")
print(f"Algo: LEC+SOEA No. of vertices: {len(config.graph)} Span: {results[1][0]} Rel: {results[1][1]} Energy: {results[1][2]} Fails: {fails[1]}")
print(f"Algo: MR+SOEA No. of vertices: {len(config.graph)} Span: {results[2][0]} Rel: {results[2][1]} Energy: {results[2][2]} Fails: {fails[2]}")
print(f"Algo: ESRG No. of vertices: {len(config.graph)} Span: {results[3][0]} Rel: {results[3][1]} Energy: {results[3][2]} Fails: {fails[3]}")
print(f"Algo: ODS+SOEA No. of vertices: {len(config.graph)} Span: {results[4][0]} Rel: {results[4][1]} Energy: {results[4][2]} Fails: {fails[4]}")
print(f"Algo: WANMS+SOEA No. of vertices: {len(config.graph)} Span: {results[5][0]} Rel: {results[5][1]} Energy: {results[5][2]} Fails: {fails[5]}")

algos = ["HEFT", "LEC", "MR", "ESRG", "ODS", "WANMS"]

spans = [results[i][0] for i in range(len(results))]
rels = [results[i][1] for i in range(len(results))]
energy = [results[i][2] for i in range(len(results))]

plt.subplot(1, 3, 1)
plt.bar(algos, spans, color ='blue')
# plt.xlabel("Algorithms")
plt.ylabel("Makespan")
plt.title("Makespan comparison")

plt.subplot(1, 3, 2)
plt.bar(algos, energy, color ='red')
# plt.xlabel("Algorithms")
plt.ylabel("Energy")
plt.title("Energy comparison")

plt.subplot(1, 3, 3)
plt.bar(algos + ["Constraint"], rels + [rel_constraint/args.itr], color ='maroon')
# plt.xlabel("Algorithms")
plt.ylabel("Rel")
plt.title("Reliability comparison")


plt.show()


