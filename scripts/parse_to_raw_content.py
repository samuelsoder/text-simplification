import json
import os
import shutil
import sys
import time
from typing import TextIO


def add_raw_content(target_file: TextIO, sequence: str):
    obj = {'raw_content': sequence}
    json_line = json.dumps(obj, ensure_ascii=False) + '\n'
    target_file.write(json_line)


def parse_to_raw_content(source_base_name: str, target_dir: str):
    """Function for parsing the files in the source_dir to files with objects
    like { raw_content: *text* } to accommodate MUSS input. Parsed files
    stored in target_dir."""

    start_time = time.time()
    file_no = 0
    no_sequences = 0

    while True:
        try:
            source_file = open(f'{source_base_name}{file_no}.txt')
            target_file = open(f'{target_dir}/raw_content_{file_no}', 'w')

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
    try:
        source_dir = args[1]
        target_dir = args[2]
    except IndexError:
        source_dir = f'{os.path.dirname(os.path.abspath(__file__))}/../out/splits/split_'
        target_dir = f'{os.path.dirname(os.path.abspath(__file__))}/../out/raw_content'

    try:
        shutil.rmtree(target_dir)
    finally:
        os.mkdir(target_dir)
        parse_to_raw_content(source_dir, target_dir)


if __name__ == '__main__':
    main()
