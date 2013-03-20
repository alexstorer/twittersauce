import twitter
import json
import pickle
import time
import random
import sys
import csv
import twitter__login

# log in, and collect statuses containing a keyword
twitter_stream = twitter__login.login_stream()
res = twitter_stream.statuses.filter(track='obama')

# store the tweets in a list
reslist = []

# keep the possible metadata in a set
tweetfields = set([u'favorited', u'in_reply_to_user_id', u'contributors', u'truncated', u'text', u'in_reply_to_status_id', u'user', u'geo', u'id', u'possibly_sensitive', u'retweeted_status', u'filter_level', u'created_at', u'retweeted', u'coordinates', u'in_reply_to_user_id_str', u'entities', u'in_reply_to_status_id_str', u'in_reply_to_screen_name', u'source', u'place', u'retweet_count', u'id_str'])

# we know that we want a few things:
# user id, followers, tweet itself, geocode

# where do we store them?
fname = '/users/astorer/Work/shoffman/example_tweets.csv'
f = open(fname,'w')
dw = csv.DictWriter(f,fieldnames=list(tweetfields))
headerd = {}
for k in list(tweetfields):
    headerd[k] = k
dw.writerow(headerd)
    #dw.writeheader()

# where do we store them?
fname = '/users/astorer/Work/shoffman/example_tweets_brief.csv'
fb = open(fname,'w')
dwb = csv.DictWriter(fb,fieldnames=['userid','tweet','followers','geocode'])
headerd = {}
for k in ['userid','tweet','followers','geocode']:
    headerd[k] = k
#dwb.writeheader()
dwb.writerow(headerd)    


# collect all of the results
for r in res:
    print len(reslist)
    reslist.append(r)
    # new versions of python
    #{k:v.encode('utf8') if isinstance(v,unicode) else v for k,v in r.items()}
    newd = {}
    for k,v in r.items():
        if isinstance(v,unicode):
            newd[k] = v.encode('utf8')
    
    #dw.writerow({k:v.encode('utf8') if isinstance(v,unicode) else v for k,v in r.items()})
    dw.writerow(newd)
    brieftext = r['text']
    if isinstance(brieftext,unicode):
        brieftext = brieftext.encode('utf8')
    briefd = {'userid':r['user']['id'],
              'tweet':brieftext,
              'followers':r['user']['followers_count'],
              'geocode':r['geo']}
    dwb.writerow(briefd)

f.close()
fb.close()