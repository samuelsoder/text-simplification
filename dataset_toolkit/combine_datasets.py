import json
import os
import random
import sys

sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}/..')
from helpers.args import find_arg


def combine_datasets(path_to_first: str, path_to_second: str, out_dir: str):
    first = json.load(open(path_to_first, encoding='utf8'))['data']
    second = json.load(open(path_to_second, encoding='utf8'))['data']

    nb_objects_first = len(first)
    nb_objects_second = len(second)

    print(f'Number of entries in first: {nb_objects_first}')
    print(f'Number of entries in second: {nb_objects_second}')

    frac = nb_objects_first / (nb_objects_first + nb_objects_second)
    index_first = 0
    index_second = 0

    first_finished = False
    second_finished = False

    out_data = []

    while not first_finished or not second_finished:
        if random.random() < frac:
            try:
                entry = first[index_first]
                entry['id'] = index_first + index_second
                out_data.append(entry)
                index_first += 1
            except IndexError:
                first_finished = True
        else:
            try:
                entry = second[index_second]
                entry['id'] = index_first + index_second
                out_data.append(entry)
                index_second += 1
            except IndexError:
                second_finished = True

    print(f'Items added: {index_first + index_second}')
    out_file = open(f'{out_dir}/combined.json', "w+", encoding='utf8')
    out = {
        'data': out_data
    }

    json.dump(out, out_file, ensure_ascii=False)
    out_file.close()


def main():
    args = sys.argv
    path_to_first = find_arg(args, '-f', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/first.json')
    path_to_second = find_arg(args, '-s', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/second.json')
    out_dir = find_arg(args, '-o', f'{os.path.dirname(os.path.abspath(__file__))}/out/combined')

    try:
        os.makedirs(out_dir)
    except FileExistsError:
        pass

    combine_datasets(path_to_first, path_to_second, out_dir)


if __name__ == '__main__':
    main()
