import json

fname = "iqssrtc_net.json"

f = open(fname)       
d = json.load(f)
f.close()

namelookup = dict()
uidlookup = dict()

for k in d:
    userd = d[k]
    if type(userd) is type(dict()):
        namelookup[userd['details']['screen_name']] = str(userd['details']['id'])
        uidlookup[str(userd['details']['id'])] = str(userd['details']['screen_name'])

adjset = set(d[namelookup['iqssrtc']]["friends"]+d[namelookup['iqssrtc']]["followers"])

fw = open('iqssrtc_net.csv','w')

for k in d:
    userd = d[k]
    if type(userd) is type(dict()):
        if userd["followers"] is not None:
            for id in userd["followers"]:
                if id in adjset:
                    source = uidlookup[str(id)]
                    dest = uidlookup[k]
                    fw.write(source+','+dest+'\n')
        if userd["friends"] is not None:
                for id in userd["friends"]:
                    if id in adjset:
                        dest = uidlookup[str(id)]
                        source = uidlookup[k]
                        fw.write(source+','+dest+'\n')

fw.close()