import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import pickle
def addvalue(dict,key,value,epoch):
    if not key in dict.keys():
        dict[key]=[[value]]
    else:
        if epoch > len(dict[key])-1:
            dict[key].append([value])
        else:
            dict[key][epoch].append(value)
def savedic(dict,fol,title='',save=True,):
    import os
    os.makedirs(fol,exist_ok=True)
    n=1
    numgraph=len(set([i.split(':')[0] for i in dict]))
    axdic={}
    fig=plt.figure()
    for key in dict:
        for e,i in enumerate(dict[key]):
            if type(i)==type([]):
                dict[key][e]=np.mean(dict[key][e])
    for key in dict:
        graph,label=key.split(':')
        showvalue=dict[key][-1]
        if graph in axdic:
            axdic[graph].plot(dict[key],label=f'{graph}:{label}:{showvalue:.2f}')
        else:
            axdic[graph]=fig.add_subplot(numgraph,1,n)
            n+=1
            axdic[graph].plot(dict[key],label=f'{graph}:{label}:{showvalue:.2f}')
    for key in axdic:
        axdic[key].legend()
    #fig.legend()
    plt.title(title)
    plt.ylim(0,1)
    fig.savefig(f'{fol}/graphs.png')
    plt.close()
    with open(f'{fol}/data.pkl','wb') as f:
        pickle.dump(dict,f)

def save(model,fol,dic,argdic,title=''):
    import json
    savedmodelpath=f'{fol}/model.pth'
    savedic(dic,'/'.join(savedmodelpath.split('/')[:-1]),title)
    torch.save(model.state_dict(), savedmodelpath)
    with open(f'{fol}/args.json','w') as f:
        json.dump(argdic,f)

