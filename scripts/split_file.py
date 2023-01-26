import os.path
import shutil
import sys
import time


def split_file(path: str, lines_per_file: int, target_dir: str):
    """Splits file at path into smaller files"""
    files_created = 0
    start_time = time.time()

    big_file = open(path)
    small_file = None
    for line_no, line in enumerate(big_file):
        if line_no % lines_per_file == 0:
            if small_file:
                small_file.close()
            small_filename = f'{target_dir}/split_{line_no // lines_per_file}.txt'
            files_created += 1
            small_file = open(small_filename, 'w')
        small_file.write(line)
    if small_file:
        small_file.close()

    result_file = open('out/splits/split_results', 'w')
    result_file.write(f'Files created: {files_created} \n')
    result_file.write(f'Lines per file: {lines_per_file} \n')
    result_file.write(f'Time taken: {time.time() - start_time} seconds')


def main():
    args = sys.argv
    target_dir = f'{os.path.dirname(os.path.abspath(__file__))}/../out/splits'
    try:
        shutil.rmtree(target_dir)
    finally:
        os.mkdir(target_dir)
        split_file(args[1], int(args[2]), target_dir)


if __name__ == '__main__':
    main()
