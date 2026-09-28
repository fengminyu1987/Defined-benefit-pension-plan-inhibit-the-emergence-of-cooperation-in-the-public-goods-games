import networkx as nx
import numpy as np
import random
import json
import matplotlib.pyplot as plt
from decimal import Decimal
L = 50
G = nx.generators.lattice.grid_2d_graph(L, L, periodic=True)
fun_fc = lambda x: (G.number_of_nodes()-sum(list(map(lambda x: x[-1], list(x.values())))))/G.number_of_nodes()
# update strategy
def update(i, j, G, strategy, c,r):
    # if (0 < random.uniform(0, 1) < 0.98):
    prob = 1 / (1 + np.exp( (get_payoffindividual(i, G, strategy,c,r,mu,alpha,payoff,centerpayoff) - get_payoffindividual(j, G, strategy,c,r,mu,alpha,payoff,centerpayoff)) / 0.1) )
    if 0<random.uniform(0, 1)<prob:
        return strategy[j][-1]
    else:
        return strategy[i][-1]
# get average payoff
def avn_payoff(G, payoff):
    n_payoff = 0
    num_nodes = nx.number_of_nodes(G)
    for i in G.nodes:
        n_payoff += payoff[i]
    avn_pf = round(( n_payoff / num_nodes),4)
    return avn_pf
# get player's loyalty
def loyalty(i, strategy):
    c_times=0
    for a in strategy[i]:
        if a == 0:
            c_times += 1
    i_loyalty = round ((c_times / len(strategy[i])),4)
    return i_loyalty

# 元组转为字符串
def tuple_to_str(key):
    if isinstance(key, tuple):
        return ','.join(str(element) for element in key)
    return key

#5 players' payoff of center i
def get_payoffcenter(i, G, strategy,c,r):
    neighbors = list(G.neighbors(i))
    Nc = 0
    result = 0
    for j in neighbors:
        if strategy[j][-1] == 0:
            Nc += 1
    if strategy[i][-1] == 0:
        Nc += 1
    result += (Nc * r * c) / 5
    result1 = round(result,4)
    return result1
# all payoff of i
def get_payoffindividual(i, G, strategy,c,r,mu,alpha,payoff,centerpayoff):
    neighbors = list(G.neighbors(i))
    result = 0
    res = 0
    strs = 0
    for j in neighbors:
        re = centerpayoff[j]
        res += re
        strs += strategy[j][-1]
    if strategy[i][-1] == 0:
        # if alpha == 0:
        #     result = res + centerpayoff[i] - c * 5
        # elif alpha != 0:
        if strs<4:
            result = res + centerpayoff[i] - c * 5 - alpha * 5
        if strs>=4:
            result = res + centerpayoff[i] - c*5 + mu * loyalty(i, strategy) * avn_payoff(G,payoff) * 5
            # result = res + centerpayoff[i] - c * 5 + mu  * avn_payoff(G, payoff) * 5
    if strategy[i][-1] == 1:
        result = res + centerpayoff[i]
    result1 = round(result, 4)
    return result1

alphalist = [0,0.1,0.3,0.5,0.7,0.9]
# alpha = 0.0
mu = 0.1
# r = 5
# rlist=[3.8,4,4.2,4.4,4.8]
# rlist=np.arange(3.6, 6.2, 0.2)
rlist=np.arange(3.5, 6.6, 0.1)
T = 400
c = 1
avg=3
colour = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black']
for kk in range(6):
    reslut = {}
    avg_payoffs= {}
    alpha=alphalist[kk]
    for k in range(31):
        r=rlist[k]
        f_c = 0
        p_f = 0
        for averagy in range(avg):
            all_payoff = []
            strategy = {}
            centerpayoff = {}
            payoff = {}
            fc = []
            x_time = []
            for i in G.nodes:
                payoff[i] = 0
                centerpayoff[i] = 0
                if (0 < random.uniform(0, 1) < 0.5):
                    strategy[i] = [0]
                else:
                    strategy[i] = [1]
            fc.append(fun_fc(strategy))
            for t in range(T):
                if (0<fc[-1]<1):
                    for i in G.nodes:
                        centerpayoff[i] = get_payoffcenter(i, G, strategy,c,r)
                        payoff[i] = get_payoffindividual(i, G, strategy,c,r,mu,alpha,payoff,centerpayoff)
                        j = random.choice(list(G.neighbors(i)))
                        strategy[i].append(update(i, j, G, strategy, c,r))
                fc.append(fun_fc(strategy))
                all_payoff.append(avn_payoff(G, payoff))
            print("\r  avg:{:d},r: {:.2f},mu: {:.2f},alpha: {:.2f},t: {:d}, fc: {:.4f}".format(averagy,r,mu,alpha, t, fc[-1]), end="     ")
            f_c +=round(np.mean(fc[-100:]),3)
            p_f += round(np.mean(all_payoff[-100:]), 3)
        reslut['alpha: {:.2f}, r: {:.2f}'.format(alpha, r)] = round(f_c/avg,3)
        avg_payoffs['alpha: {:.2f}, r: {:.2f}'.format(alpha, r)] = round(p_f/avg,3)
    json_res1 = json.dumps(reslut)
    json_res2 = json.dumps(avg_payoffs)
    with open('.\\saves\\newfor\\fc_rANDpayoff\\fc_r2\\defnei4_fc_r_alpha{:.2f}.json'.format(alpha), 'w') as json_file1:
        json_file1.write(json_res1)
    with open('.\\saves\\newfor\\fc_rANDpayoff\\payoff_r2\\defnei4_pf_r_alpha{:.2f}.json'.format(alpha), 'w') as json_file2:
        json_file2.write(json_res2)
#     plt.plot(x_time, fc, color=colour[rlist.index(k)], label=("alpha="+str(alpha)))
# plt.xlabel("t", fontdict={'size': 16})
# plt.ylabel("fc", fontdict={'size': 16})
# plt.legend(fontsize=8,loc='upper left',frameon=False)
# plt.legend(fontsize=10,loc='upper left', bbox_to_anchor=(1, 1))
# plt.show()



