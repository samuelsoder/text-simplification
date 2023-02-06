import gzip
import json
import os
import shutil
import sys
import time
from typing import TextIO


def try_arg(args, index, default):
    try:
        val = args[index]
    except IndexError:
        val = default
    return val


def add_raw_content(target_file: TextIO, sequence: str):
    obj = {'raw_content': sequence}
    json_line = json.dumps(obj, ensure_ascii=False) + '\n'
    target_file.write(json_line)


def parse_to_raw_content(source_base_name: str, target_dir: str, language='sv'):
    """Function for parsing the files in the source_dir to files with objects
    like { raw_content: *text* } to accommodate MUSS input. Parsed files
    stored in target_dir."""

    start_time = time.time()
    file_no = 0
    no_sequences = 0

    while True:
        try:
            source_file = open(f'{source_base_name}{file_no}.txt')
            target_file = gzip.open(f'{target_dir}/{language}_head_{file_no:04d}.json.gz', 'wt', encoding='utf-8')

            sequence = ''

            while True:
                line = source_file.readline()
                if len(line) == 0:
                    if len(sequence) != 0:
                        add_raw_content(target_file, sequence)
                        no_sequences += 1
                    break

                if line != '\n':
                    sequence += line

                if line == '\n':
                    add_raw_content(target_file, sequence)
                    no_sequences += 1
                    sequence = ''
                    continue

            source_file.close()
            target_file.close()
            file_no += 1
        except FileNotFoundError:
            break

    result_file = open(f'{target_dir}/parse_results', 'w')
    result_file.write(f'Files parsed: {file_no} \n')
    result_file.write(f'Number of sequences parsed: {no_sequences} \n')
    result_file.write(f'Time taken: {time.time() - start_time} seconds')


def main():
    args = sys.argv

    source_base = try_arg(args, 1, f'{os.path.dirname(os.path.abspath(__file__))}/../out/splits/split_')
    target_dir = try_arg(args, 2, f'{os.path.dirname(os.path.abspath(__file__))}/../out/raw_content')

    try:
        shutil.rmtree(target_dir)
    finally:
        os.makedirs(target_dir)
        parse_to_raw_content(source_base, target_dir)


if __name__ == '__main__':
    main()
