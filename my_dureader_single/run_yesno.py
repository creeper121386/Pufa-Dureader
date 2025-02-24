import os 
import torch 
import numpy as np
import torch.nn as nn
import my_rc_model
from dataset import BRCDataset
import pickle
from run import gen_yesno_vec
VOCAB_PATH = '../data/vocab_search_pretrain/vocab.data'
train_files = '../data/yesno/data_train_preprocessed.json'
dev_files = '../data/yesno/data_dev_preprocessed.json'
q_len = 24
p_len = 209
BATCH_SIZE = 16

class FC(nn.Module):
    def __init__(self):
        super(FC, self).__init__()
        self.fc1 = nn.Sequential([
            nn.Linear()
        ])

def load():
    para_path = '../data/para.npy'
    qua_path = '../data/qua.npy'
    if not os.path.exists(para_path) and os.path.exists(qua_path):
        print('data files not exist, generate new data...')
        gen_yesno_vec()
    para = np.load(para_path)
    qua = np.load(qua_path)
    return para, qua


def preproc(para, qua):
    size = p_len+q_len
    data = torch.ones((len(para), BATCH_SIZE, size))
    j = 0
    for p, q in zip(para, qua):
        new = np.zeros((BATCH_SIZE, size))
        i = 0
        for pp, qq in zip(p, q):
            tmp = np.append(pp, qq)
            real_len = len(tmp)
            if real_len > size:
                new[i] = tmp[:size]
            else:
                new[i] = np.append(tmp, np.zeros(size-real_len))
            i +=1
        data[j] = torch.FloatTensor(new)
        j += 1
    return data


def run_yesno():
    para, qua = load()
    data = preproc(para, qua)

    


if __name__ == '__main__':
    run_yesno()
    
    