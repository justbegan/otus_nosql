import json
import redis
import time


r = redis.Redis(host='localhost', port=6379, db=0)

with open('data.json', 'r') as f:
    data = json.load(f)

r.flushdb()

report = {}


def measure_time(write_func, read_func):
    start_time = time.time()
    write_func()
    write_time = time.time() - start_time

    start_time = time.time()
    read_func()
    read_time = time.time() - start_time

    return write_time, read_time


def write_string():
    r.set('json_string', json.dumps(data))


def read_string():
    json_string = r.get('json_string')
    json.loads(json_string)


report['String'] = measure_time(write_string, read_string)


def write_hash():
    for index, item in enumerate(data):
        r.hset(f'json_hash_{index}', mapping={k: json.dumps(v) for k, v in item.items()})


def read_hash():
    for index in range(len(data)):
        r.hgetall(f'json_hash_{index}')


report['Hash'] = measure_time(write_hash, read_hash)


def write_zset():
    for index, item in enumerate(data):
        r.zadd('json_zset', {json.dumps(item): index})


def read_zset():
    json_zset = r.zrange('json_zset', 0, -1)
    [json.loads(item) for item in json_zset]


report['ZSet'] = measure_time(write_zset, read_zset)


def write_list():
    for item in data:
        r.rpush('json_list', json.dumps(item))


def read_list():
    json_list = r.lrange('json_list', 0, -1)
    [json.loads(item) for item in json_list]


report['List'] = measure_time(write_list, read_list)

# Печать отчета
print(json.dumps(report, indent=4))
