import twitter
import json
import pickle
import time
import random
import sys
import csv

twitter_stream = twitter.TwitterStream(auth=UserPassAuth('iqssrtc', '********'))
res = twitter_stream.statuses.filter(track='obama')

reslist = []

tweetfields = set()

for r in res:
    if len(reslist)<5000:
        print len(reslist)
        reslist.append(r)
        tweetfields = tweetfields.union(r.keys())
    else:
        break

fname = '/users/astorer/Work/presentations/twitter/example_tweets.csv'
f = open(fname,'w')
dw = csv.DictWriter(f,fieldnames=list(tweetfields))
dw.writeheader()

for r in reslist:
    dw.writerow({k:v.encode('utf8') if isinstance(v,unicode) else v for k,v in r.items()})


f.close()
