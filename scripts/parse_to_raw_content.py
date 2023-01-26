import os
import shutil
import time


def parse_to_raw_content(source_dir: str, target_dir: str):
    start_time = time.time()
    file_no = 0

    while True:
        try:
            source_file = open('{}/split_{}.txt'.format(source_dir, file_no))
            file_no += 1
            source_file.close()
        except FileNotFoundError:
            break

    result_file = open('out/raw_content/split_results', 'w')
    result_file.write('Files parsed: {} \n'.format(file_no))
    result_file.write('Time taken: {} seconds'.format(time.time() - start_time))


def main():
    source_dir = '{}/../out/splits'.format(os.path.dirname(os.path.abspath(__file__)))
    target_dir = '{}/../out/raw_content'.format(os.path.dirname(os.path.abspath(__file__)))
    try:
        shutil.rmtree(target_dir)
    finally:
        os.mkdir(target_dir)
        parse_to_raw_content(source_dir, target_dir)


if __name__ == '__main__':
    main()
