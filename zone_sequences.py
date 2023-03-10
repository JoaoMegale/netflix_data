import json
import numpy as np
import pandas as pd
from collections import Counter

def Get_Pitch_Zone(x, y):
    if x < 20.15:
        if y <= 13.84:
            return 1
        if y > 13.84 and y <= 54.16:
            return 2
        else:
            return 3
    elif x < 36.325:
        if y <= 13.84:
            return 4
        if y > 13.84 and y <= 24.84:
            return 5
        if y > 24.84 and y <= 43.16:
            return 6
        if y > 43.16 and y <= 54.16:
            return 7
        else:
            return 8
    elif x < 52.5:
        if y <= 13.84:
            return 9
        if y > 13.84 and y <= 24.84:
            return 10
        if y > 24.84 and y <= 43.16:
            return 11
        if y > 43.16 and y <= 54.16:
            return 12
        else:
            return 13
    elif x < 68.675:
        if y <= 13.84:
            return 14
        if y > 13.84 and y <= 24.84:
            return 15
        if y > 24.84 and y <= 43.16:
            return 16
        if y > 43.16 and y <= 54.16:
            return 17
        else:
            return 18
    elif x < 84.85:
        if y <= 13.84:
            return 19
        if y > 13.84 and y <= 24.84:
            return 20
        if y > 24.84 and y <= 43.16:
            return 21
        if y > 43.16 and y <= 54.16:
            return 22
        else:
            return 23
    else:
        if y <= 13.84:
            return 24
        if y > 13.84 and y <= 24.84:
            return 25
        if y > 24.84 and y <= 43.16:
            return 26
        if y > 43.16 and y <= 54.16:
            return 27
        else:
            return 28

with open(r'C:\Users\jotal\IC\Wyscout\events_England.json') as f:
    data = json.load(f)
df = pd.DataFrame(data)

all_sequences = []
chute = False
num_seq = 0
sequences = np.array([], dtype=object)
zone = Get_Pitch_Zone(df['positions'][0][0]['x'], df['positions'][0][0]['y'])
seq = str(zone)
conta = 0

for i in range(1, len(df)):
    conta += 1
    try:
        zone = Get_Pitch_Zone(df['positions'][i][0]['x'], df['positions'][i][0]['y'])
        if (df['teamId'][i - 1] == df['teamId'][i]) and (df['matchId'][i - 1] == df['matchId'][i]) and (df['matchPeriod'][i - 1] == df['matchPeriod'][i]):
            seq += ' ' + str(zone)
        else:
            if chute == True:
                sequences = np.insert(sequences, num_seq, seq)
                num_seq += 1
            all_sequences.append(seq)
            chute = False
            seq = str(zone)
        if df['eventName'][i] == 'Shot':
            chute = True
    except IndexError:
        if chute == True:
            sequences = np.insert(sequences, num_seq, seq)
            num_seq += 1
        all_sequences.append(seq)
        chute = False
        seq = str(zone)
        if df['eventName'][i] == 'Shot':
            chute = True

for i in range(len(sequences)):
    sequences[i] = list(map(int, sequences[i].split(" ")))

for i in range(len(sequences)):
    if len(sequences[i]) <= 1:
        sequences[i] = np.nan

long_sequences = sequences[~pd.isnull(sequences)]
for i in range(len(long_sequences)):
    long_sequences[i] = " ".join(str(n) for n in long_sequences[i])
    
counts = Counter(long_sequences)                                 
frequentes = counts.most_common(10)