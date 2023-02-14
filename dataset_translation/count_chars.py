import time
import os
import sys
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}/..')
from dataset_translation.helpers.args import find_arg


def count_chars(source_file, target_dir):
    start_time = time.time()

    words = 0
    chars = 0
    with open(source_file) as file:
        while True:
            line = file.readline()
            if len(line) == 0:
                break
            words += len(line.split(' '))
            chars += len(line)

    result_file = open(f'{target_dir}/results.txt', 'w+')
    result_file.write(f'Number of words: {words} \n')
    result_file.write(f'Number of characters: {chars} \n')
    result_file.write(f'Time taken: {time.time() - start_time} seconds\n')
    result_file.close()


def main():
    args = sys.argv
    source_file = find_arg(args, '-s', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/small_test.txt')
    target_dir = find_arg(args, '-t', f'{os.path.dirname(os.path.abspath(__file__))}/out/counted')

    try:
        os.makedirs(target_dir)
    except FileExistsError:
        pass

    count_chars(source_file, target_dir)


if __name__ == '__main__':
    main()