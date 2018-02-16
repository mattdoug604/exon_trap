#!/home2/mattdoug/python3/bin/python3
# Last updated: 5/2/2018
# Author: Matt Douglas

from __future__ import print_function
import argparse, sys

def pprint(*args, **kwargs):
    level = kwargs.pop('level', {'level':None})
    if level == 'debug':
        if DEBUG:
            print(*args, **kwargs)
    else:
        if not QUIET:
            print(*args, **kwargs)


def parse_index(args):
    global QUIET
    global DEBUG
    QUIET = args.quiet
    DEBUG = args.debug
    PREFIX = args.prefix
    index_path = args.index
    region = args.region
    index_f = {}
    index_r = {}
    start_c = 0
    end_c = 0

    pprint('Parsing reference index...', end='')
    for i in range(6):
        index = index_path + '.' + str(i+1)
        with open(index, 'r') as f:
            for line in f:
                line = line.strip().split('\t')
                if len(line) < 3: #if no start/stop codons were found, the 3rd column may be empty
                    continue
                chrom, kind, pos_list = line
                chrom = str(chrom)
                kind  = int(kind)
                # if the feature is outside the specified region, skip it
                if region is not None and chrom != region[0]:
                    continue
                pos_list = list(map(int, pos_list.split(',')))
                if region is not None:
                    temp = []
                    for n in pos_list:
                        if region[1] <= n <= region[2]:
                            temp.append(n)
                    pos_list = temp
                # add the features to the dictionaries
                d = [index_f if i < 3 else index_r][0] # 1 == "+", -1 == "-"
                frame = [i-3 if i >= 3 else i][0]
                try:
                    d[chrom][frame] += [(x, kind) for x in pos_list]
                except KeyError:
                    d[chrom] = [ [], [], [] ]
                    d[chrom][frame] += [(x, kind) for x in pos_list]
                # update the counters
                if kind == 0:
                    start_c += len(pos_list)
                elif kind == 3:
                    end_c += len(pos_list)
    pprint('\rParsing reference index... Done!')
    pprint('  {:,} putative start codons'.format(start_c))
    pprint('  {:,} stop codons'.format(end_c))

    return index_f, index_r
