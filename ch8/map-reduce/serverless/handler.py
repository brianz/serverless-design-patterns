import sys

from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

import mapreduce.mapper
import mapreduce.reducer


def driver(event, context):
    prefix = event or 'tiny'

    bucket_name = 'big-data-benchmark'

    if prefix == 'large':
        mapreduce.mapper.crawl(bucket_name, prefix='pavlo/text/1node/uservisits/part-')
    else:
        mapreduce.mapper.crawl(bucket_name, prefix='pavlo/text/tiny/uservisits/part-')


def mapper(event, context):
    mapreduce.mapper.map(event)


def reducer(event, context):
    mapreduce.reducer.reduce(event)


def final_reducer(event, context):
    print(event)
    #mapreduce.reducer.final_reduce(event)
