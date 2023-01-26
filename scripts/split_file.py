import os.path
import shutil
import sys
import time


def split_file(path: str, lines_per_file: int, target_dir: str):
    files_created = 0
    start_time = time.time()

    big_file = open(path)
    small_file = None
    for line_no, line in enumerate(big_file):
        if line_no % lines_per_file == 0:
            if small_file:
                small_file.close()
            small_filename = '{}/split_{}.txt'.format(target_dir, line_no // lines_per_file)
            files_created += 1
            small_file = open(small_filename, 'w')
        small_file.write(line)
    if small_file:
        small_file.close()

    result_file = open('out/splits/split_results', 'w')
    result_file.write('Files created: {} \n'.format(files_created))
    result_file.write('Lines per file: {} \n'.format(lines_per_file))
    result_file.write('Time taken: {} seconds'.format(time.time() - start_time))


def main():
    args = sys.argv
    target_dir = '{}/../out/splits'.format(os.path.dirname(os.path.abspath(__file__)))
    try:
        shutil.rmtree(target_dir)
    finally:
        os.mkdir(target_dir)
        split_file(args[1], int(args[2]), target_dir)


if __name__ == '__main__':
    main()
