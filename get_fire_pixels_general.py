from cmr import GranuleQuery
import os.path as osp
import subprocess

_token = '' #user token from LAADS

cases = [
    [('2021-07-18T00:00:00Z','2021-07-22T00:00:00Z'), (-119.959631,-119.474474,38.615075,38.801624)], #start time. end time, bounding box
    #...
]
for time,bounds in cases:
    api = GranuleQuery()
    lonmin,lonmax,latmin,latmax = bounds
    bbox = [(lonmin,latmax),(lonmin,latmin),(lonmax,latmin),(lonmax,latmax),(lonmin,latmax)]
    search = api.parameters(
        short_name='MOD14',
        downloadable=True,
        polygon=bbox,
        temporal=time)
    metas = api.get(search.hits())
    metas = [m for m in metas if m['collection_concept_id'] == 'C193529945-LPDAAC_ECS']
    for meta in metas:
        url = meta['links'][0]['href']
        if not osp.exists(osp.basename(url)):
            command = ['wget','--header=\'Authorization: Bearer %s\'' % _token, url]
            print('>>>>    Running {}'.format(' '.join(command)))
            subprocess.call(' '.join(command),shell=True)