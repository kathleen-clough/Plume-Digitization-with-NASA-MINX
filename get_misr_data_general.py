import re
import requests
import subprocess
import os.path as osp
from datetime import datetime,timedelta 

_base_url = 'https://asdc.larc.nasa.gov/data/MISR/{}/'
_products = 'MI1B2E.003, MIL2ASAE.002, MIL2ASAE.003, MIB2GEOP.002, MI1B2T.003, MIL2TCCL.003'.split(', ')
_tags = 'MISR_AM1_GRP_ELLIPSOID_GM, MISR_AM1_AS_AEROSOL, MISR_AM1_AS_AEROSOL, MISR_AM1_GP_GMP, MISR_AM1_GRP_TERRAIN_GM, MISR_AM1_TC_CLASSIFIERS'.split(', ')
_token = '' #user token from LAADS
start_time = datetime(2021,7,17)
end_time = datetime(2021,10,25)
orbits = '115414,116244'.split(', ') #put as many orbits as needed separated by a comma

paths = []
dt = timedelta(days=1)
time = start_time
while time <= end_time:
    print('>> Processing time {}'.format(time))
    for tag,product in zip(_tags,_products):
        print('>>>  Processing product {}'.format(product))
        url = osp.join(_base_url.format(product),'{:04d}.{:02d}.{:02d}/'.format(time.year,time.month,time.day))
        r = requests.get(url, headers={"Authorization": "Bearer {}".format(_token)})
        for orbit in orbits:
            search = '>('+tag+'_P[0-9]{3}_O'+orbit+'(?:_[A-Z]{2})?'+'_F[0-9]{2}_[0-9]{4}\.(?:hdf|nc))<'
            s = re.findall(r'{}'.format(search),str(r.content))
            if len(s):
                print('>>>    Processing orbit {}'.format(orbit))
                for f in s:
                    if not osp.exists(f):
                        path = re.search(r'_P[0-9]{3}_',f)
                        if path not in paths:
                            paths.append(path)
                        command = ['wget','--header=\'Authorization: Bearer %s\'' % _token, osp.join(url,f)]
                        print('>>>>    Running {}'.format(' '.join(command)))
                        subprocess.call(' '.join(command),shell=True)
    time += dt

for folder in ['1999.11.07/','1999.11.08/']:
    r = requests.get(osp.join(_base_url.format('MIANCAGP.001'),folder), headers={"Authorization": "Bearer {}".format(_token)})
    for path in paths:
        search = '>(MISR_AM1_AGP_P{}'.format(path)+'_F[0-9]{2}_[0-9]{2}\.hdf)<'
        s = re.findall(r'{}'.format(search),str(r.content))
        if len(s):
            for f in s:
                command = ['wget','--header=\'Authorization: Bearer %s\'' % _token, osp.join(url,f)]
                print('>>>>    Running {}'.format(' '.join(command)))
                subprocess.call(' '.join(command),shell=True)
