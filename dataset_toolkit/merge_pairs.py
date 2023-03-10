import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from helpers.args import find_arg


def merge_to_pairs(path_to_src: str, path_to_dst: str, target_dir: str):
    sentences = 0

    src_file = open(path_to_src)
    dst_file = open(path_to_dst)
    out_file = open(f'{target_dir}/merged.out', 'w')

    while True:
        src_line = src_file.readline()
        dst_line = dst_file.readline()

        if len(src_line) == 0:
            break

        entry = {
            'id': sentences,
            'src': src_line,
            'dst': dst_line,
        }

        out_file.write(str(entry))

        sentences += 1

    src_file.close()
    dst_file.close()
    out_file.close()


def main():
    args = sys.argv

    src_file = find_arg(args, '-s', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/test_src.txt')
    dst_file = find_arg(args, '-d', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/test_dst.txt')
    out_dir = find_arg(args, '-d', f'{os.path.dirname(os.path.abspath(__file__))}/out/merged')

    try:
        shutil.rmtree(out_dir)
    finally:
        os.makedirs(out_dir)
        merge_to_pairs(src_file, dst_file, out_dir)


if __name__ == '__main__':
    main()
