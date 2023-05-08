import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}/../..')
from helpers.args import find_arg


def get_vals(source):
    origs = []
    simplified = []
    diff = []
    change = []

    with open(source) as file:
        line = file.readline()
        while line:
            vals = line.split(',')
            origs.append(float(vals[0]))
            simplified.append(float(vals[1]))
            diff.append(float(vals[2]))
            change.append(float(vals[3]) * 100)

            line = file.readline()

    return origs, simplified, diff, change


def analyse(source):
    origs, simplified, diff, change = get_vals(source)

    diff_avg = np.average(diff)
    diff_var = np.var(diff)
    diff_std = np.std(diff)

    change_avg = np.average(change)
    change_var = np.var(change)
    change_std = np.std(change)

    print(diff_avg, diff_std, change_avg, change_std)


def main():
    args = sys.argv

    source_file = find_arg(args, '-s',
                           f'{os.path.dirname(os.path.abspath(__file__))}/../out/evaluation/asset.sv.test.orig.simplified.fully.combined.lix')

    analyse(source_file)


if __name__ == '__main__':
    main()

