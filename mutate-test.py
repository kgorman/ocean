#!/usr/bin/env python

import json
import pprint
import random
import dateutil.parser

from datetime import timedelta

def rand_choice():
    choice = random.randint(0, 1)
    if choice == 1:
        return True
    return False

def mutate_ts(data, sec_max=300):
    ts   = dateutil.parser.parse(data)
    rand = random.randint(1, sec_max)
    if rand_choice():
        return ts + timedelta(seconds=rand)
    else:
        return ts - timedelta(seconds=rand)

def mutate(data):
    if isinstance(data, dict):
        ret = {}
        for key in data.keys():
            ts_keys   = ['t', 'fetch_date']
            skip_keys = ['id', 'loc', 'name', 'station_id']
            if key in ts_keys:
                ret[key] = mutate_ts(data[key])
            elif key in skip_keys:
                ret[key] = data[key]
            else:
                ret[key] = mutate(data[key])
        return ret
    elif isinstance(data, list):
        ret = []
        for item in data:
            ret.append(mutate(item))
        return ret
    elif isinstance(data, (int,long)):
        rand = random.randint(1, 8)
        if rand_choice():
            return data + rand
        return data - rand
    elif isinstance(data, float):
        rand = random.uniform(1.001, 1.6)
        if rand_choice():
            return data + rand
        return data - rand
    else:
        return data

def amplify(data, num_times=1):
    count = 0
    report_data = [data]
    while count < num_times:
        report_data.append(mutate(data))
        count += 1
    return report_data 

try:
    f = open("mutate-test.json")
    data = json.loads(f.read())
except Exception, e:
    print "FAILED: %s" % e
    raise e

# tests:
#print amplify("test")
#print amplify(1)
#print amplify(1.0)
#print amplify([1.0,0.1])
#print amplify({'test':[1.0,0.1]})
#print amplify({'test':{'one':{'two':'three', 'four':5}}})

# Return 'data' plus 3 x mutated copies in an array
pprint.pprint(amplify(data, 3))
