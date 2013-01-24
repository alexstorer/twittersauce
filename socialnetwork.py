import twitter
import json
import pickle
import time
import random
import sys

import twitter__login

def timer15():
    for i in range(1,16):
        print "Waiting minute", i, "of 15"
        time.sleep(60)

def crawlUser(user_id,d,t):
    addUser(user_id,d,t)
    user_id_str = str(user_id)    
    for uid in d[user_id_str]["followers"]:
        addUser(uid,d,t)
    for uid in d[user_id_str]["friends"]:
        addUser(uid,d,t)

def addUser(user_id,d,t):
    user_id_str = str(user_id)
    if user_id_str in d.keys():
        print "Already have user", user_id_str, " (", d[user_id_str]["details"]["screen_name"],")"
        if "details" not in d[user_id_str].keys():
            d[user_id_str]["details"] = users_show(t,user_id=user_id)
        if (d[user_id_str]["details"]['followers_count'] > 15000 or
            d[user_id_str]["details"]['friends_count'] > 15000):
            print "Too many friends/followers: ", user_id_str, " (", d[user_id_str]["details"]["screen_name"],")"
            specialcases.append(user_id_str)
        else:
            if ("followers" not in d[user_id_str].keys()):
                d[user_id_str]["followers"] = followers_ids(t,user_id=user_id)
            if ("friends" not in d[user_id_str].keys()):
                d[user_id_str]["friends"] = followers_ids(t,user_id=user_id)
    else:
        print "Downloading user", user_id_str        
        userd = dict()
        userd["details"] = users_show(t,user_id=user_id)
        print "================> ", userd["details"]["screen_name"]
        if (userd["details"]['followers_count'] > 15000 or
            userd["details"]['friends_count'] > 15000):
            print "Too many friends/followers: ", user_id_str, " (", userd["details"]["screen_name"],")"
            specialcases.append(user_id_str)
        else:
            userd["followers"] = followers_ids(t,user_id=user_id)
            userd["friends"] = friends_ids(t,user_id=user_id)
        d[user_id_str] = userd
    if random.random()>0.0:
        saveFile(d)
        
        
def users_show(t,user_id=None,screen_name=None,wait_period=2):
    try:
        if user_id is not None:
            return t.users.show(user_id=user_id)
        elif screen_name is not None:
            return t.users.show(screen_name=screen_name)
    except twitter.api.TwitterHTTPError as e:
        wait_period = handleTwitterHTTPError(e, t, wait_period)
        if wait_period is not None:
            return users_show(t,user_id=user_id,screen_name=screen_name,wait_period=wait_period)
        else:
            return None

def followers_ids(t,user_id=None,screen_name=None,wait_period=2,cursor=-1):
    try:
        if user_id is not None:
            result = t.followers.ids(user_id=user_id,cursor=cursor)
        elif screen_name is not None:
            result = t.followers.ids(screen_name=screen_name,cursor=cursor)
    except twitter.api.TwitterHTTPError as e:
        wait_period = handleTwitterHTTPError(e, t, wait_period)
        if wait_period is not None:
            return followers_ids(t,user_id=user_id,screen_name=screen_name,wait_period=wait_period,cursor=cursor)
        else:
            return None            
    if result["next_cursor"] != 0:
        allids = result['ids']
        return allids+followers_ids(t,user_id=user_id,screen_name=screen_name,wait_period=wait_period,cursor=result["next_cursor"])
    else:
        return result['ids']

def friends_ids(t,user_id=None,screen_name=None,wait_period=2,cursor=-1):
    try:
        if user_id is not None:
            result = t.friends.ids(user_id=user_id,cursor=cursor)
        elif screen_name is not None:
            result = t.friends.ids(screen_name=screen_name,cursor=cursor)
    except twitter.api.TwitterHTTPError as e:
        wait_period = handleTwitterHTTPError(e, t, wait_period)
        if wait_period is not None:
            return friends_ids(t,user_id=user_id,screen_name=screen_name,wait_period=wait_period,cursor=cursor)
        else:
            return None
    if result["next_cursor"] != 0:
        allids = result['ids']
        return allids+friends_ids(t,user_id=user_id,screen_name=screen_name,wait_period=wait_period,cursor=result["next_cursor"])
    else:
        return result['ids']        

def getRelationship(t,user_s,user_t,wait_period=2):
    try:
        return t.friendships.show(source_id=user_s,target_id=user_t)        
    except twitter.api.TwitterHTTPError as e:
        wait_period = handleTwitterHTTPError(e, t, wait_period)
        if wait_period is not None:
            return getRelationship(t,user_s,user_t,wait_period=wait_period)
        else:
            return None

        
def handleSpecialCases(t,d,l):
    '''
    If we have too many friends/followers, we need to collect them
    manually.
    We need to query each special case with respect to the others -
    does Al Gore follow Barack Obama?
    We then need to fill in the followers from the remainder of the
    elements in the dictionary. Does AdventureSauce1 follow Barack Obama?
    Then put it in BarackObama's field.
    '''

    # first, initialize the followers/friends lists:
    for uid in l:
        if "followers" not in d[uid].keys():
            d[uid]["followers"] = []
        if "friends" not in d[uid].keys():
            d[uid]["friends"] = []
            
    
    for i in range(0,len(l)):
        for j in range(i+1,len(l)):
            res = getRelationship(t,l[i],l[j],wait_period=2)
            if res['relationship']['source']['followed_by']:
                # l[i] is following l[j]
                d[l[j]]['followers'].append(l[i])
                d[l[i]]['friends'].append(l[j])
            if res['relationship']['source']['following']:
                d[l[i]]['followers'].append(l[j])
                d[l[j]]['friends'].append(l[i])

    # for each user that's not in the list, append their information to the special cases
    for uid in d.keys():
        if uid not in l and uid !='fname':
            for specialid in l:
                if specialid in d[uid]['friends']:
                    d[specialid]['followers'].append(uid)
                if specialid in d[uid]['followers']:
                    d[specialid]['friends'].append(uid)
        
def handleTwitterHTTPError(e, t, wait_period=2):
    if e.e.code == 401:
        print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
        return None        
    elif e.e.code in (502, 503):
        # these errors are Twitter's fault!
        print >> sys.stderr, 'Encountered %i Error. Will retry in %i seconds' % (e.e.code,
                wait_period)
        time.sleep(wait_period)
        wait_period *= 1.5
        return wait_period
    elif e.e.code == 429:
        # you are being rate limited
        print 'Rate limiting.'
        timer15()
        return wait_period
    else:
        raise e

def getFile(fname):
    try:
        f = open(fname)       
        d = json.load(f)
        f.close()
        return d
    except:
        return None

def saveFile(d):
    print "Saving!"
    f = open(d["fname"],'w')    
    json.dump(d,f)
    f.close()
            
t = twitter__login.login()
screen_name = 'AdventureSauce1'
response = t.users.show(screen_name=screen_name)
user_id = response['id']

dname = screen_name+'_net.json'

d = getFile(dname)
if d is None:
    d = dict()
    d["fname"] = dname

specialcases = []
crawlUser(user_id,d,t)
handleSpecialCases(t,d,specialcases)
saveFile(d)