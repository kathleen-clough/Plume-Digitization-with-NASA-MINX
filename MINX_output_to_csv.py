import glob
import os.path as osp
import pandas as pd
import re
import numpy as np

f_path = 'creek_plume_txt_files' #path to folder with all txt files created during digitization
sep = 'RESULTS:'
list = glob.glob(osp.join(f_path, '*.txt'))
data = {'STID': [], 'point_number': [], 'file_name': [], 
        'date_time': [], 'plume_height': [], 'LONGITUDE': [], #dictionary containing all necessary columns
        'LATITUDE': [], 'ELEVATION': [], 'STATE': []}
tmp = 0
for f in list:
    txt = open(f).read()
    fltr = txt.split(sep)
    for l in fltr[0].split('\n'):
        if 'Date acquired' in l:
            date = ':'.join(l.split(':')[1:]).strip()
        if 'UTC time' in l:                               #these lines extract the date and time from the txt file
            time = ':'.join(l.split(':')[1:]).strip() 
    lines = fltr[1].split('\n')
    lines = lines[4:]
    for line in lines:
        if len(line)>10:
            cols = re.split(r'\s+', line)
            data['STID'].append('MISR_{:07d}'.format(tmp))
            data['point_number'].append(int(cols[1]))
            data['file_name'].append(osp.basename(f).split('.txt')[0])
            data['date_time'].append(date+' '+time)
            data['plume_height'].append(float(cols[11]))
            data['LONGITUDE'].append(float(cols[2]))
            data['LATITUDE'].append(float(cols[3]))
            data['ELEVATION'].append(float(cols[9]))
            data['STATE'].append('CA')
            tmp += 1
df = pd.DataFrame(data)
df['date_time'] = pd.to_datetime(df['date_time'])
df.loc[df['plume_height']==-9999.,'plume_height'] = np.nan #removal of -9999 values
df.to_csv('Creek_Final_Digitization.csv', index=False) #conversion to .csv

