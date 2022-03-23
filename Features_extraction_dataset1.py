import pandas as pd
import os
import re
import numpy as np

df_res = pd.DataFrame(columns=['cycle', 'Voltages', 'rate', 'Tem', 'Capacity'])
files = os.listdir('./Dataset_1_NCA_battery/')
for file in range(len(files)):
    Tem = int(files[file][2:4])
    data_r = pd.read_csv(os.path.join('./Dataset_1_NCA_battery/', files[file]))
    for i in range(int(np.min(data_r['cycle number'].values)), int(np.max(data_r['cycle number'].values))+1):
        data_i = data_r[data_r['cycle number'] == i]
        Ecell = np.array(data_i['Ecell/V'])
        Q_dis = np.array(data_i['Q discharge/mA.h'])
        Current = np.array(data_i['<I>/mA'])
        control = np.array(data_i['control/V/mA'])
        cr = np.array(data_i['control/mA'])[1]/3500
        if np.max(Q_dis) < 2500 or np.max(Q_dis) > 3500:
            continue
        index = np.where(np.abs(control) == 0)
        start = index[0][0]
        for j in range(3):
            if control[start+3] == 0:
                break
            else:
                start = index[0][j+1]
        if control[start+13] == 0 and Ecell[start+13] > 4.0:
            df_res = df_res.append({'cycle': i, 'Voltages': Ecell[start:start+14], 'rate': cr, 'Tem': Tem,
                                    'Capacity': np.max(Q_dis)}, ignore_index=True)

# Save to excel file
df_res.to_excel('Dataset_1_NCA_battery.xlsx', index=False)
# Or save to csv file
# df_res.to_csv('Dataset_1_NCA_battery.csv', index=False)
print('Features extraction is done')
