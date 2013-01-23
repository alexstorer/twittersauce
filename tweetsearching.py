import twitter
import twitter__login
import json
import pickle
import time
import random
import sys
import csv

t = twitter__login.login()
boston_res = t.search.tweets(q="patriots",geocode="42.350425,-71.026611,50mi",count=100)
baltimore_res = t.search.tweets(q="patriots",geocode="39.291797,-76.59668,50mi",count=100)

reslist = []
tweetfields = set()

for r in boston_res['statuses']:
    if len(reslist)<5000:
        print len(reslist)
        r['searchloc'] = 'boston'
        reslist.append(r)
        tweetfields = tweetfields.union(r.keys())
    else:
        break

for r in baltimore_res['statuses']:
    if len(reslist)<5000:
        print len(reslist)
        r['searchloc'] = 'baltimore'        
        reslist.append(r)        
        tweetfields = tweetfields.union(r.keys())
    else:
        break

        
fname = '/users/astorer/Work/presentations/twitter/nfl_tweets.csv'
f = open(fname,'w')
#dw = csv.DictWriter(f,fieldnames=list(tweetfields))
dw = csv.DictWriter(f,fieldnames=[u"text","searchloc"])
dw.writeheader()

for r in reslist:
    subd = {}
    for k in dw.fieldnames:
        if isinstance(r[k],unicode):
            subd[k] = r[k].encode('utf8')
        else:
            subd[k] = r[k]
    dw.writerow(subd)

f.close()