import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from helpers.args import find_arg


def merge_to_pairs_json(path_to_src: str, path_to_dst: str, target_dir: str):
    sentences = 0

    src_file = open(path_to_src)
    dst_file = open(path_to_dst)
    out_file = open(f'{target_dir}/merged.json', 'w+', encoding='utf8')

    output = {
        'data': []
    }

    while True:
        src_line = src_file.readline()
        dst_line = dst_file.readline()

        if len(src_line) == 0:
            break

        output['data'].append({
            'id': sentences,
            'src': src_line,
            'dst': dst_line,
        })

        sentences += 1

    json.dump(output, out_file, ensure_ascii=False)
    src_file.close()
    dst_file.close()
    out_file.close()

def merge_to_pairs_txt(path_to_src: str, path_to_dst: str, target_dir: str):
    src_file = open(path_to_src)
    dst_file = open(path_to_dst)
    out_file = open(f'{target_dir}/merged', 'w+')

    while True:
        src_line = src_file.readline()
        dst_line = dst_file.readline()

        if len(src_line) == 0:
            break

        out_file.write(src_line)
        out_file.write(f'{dst_line}\n')

    src_file.close()
    dst_file.close()
    out_file.close()


def main():
    args = sys.argv

    src_file = find_arg(args, '-s', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/test_src.txt')
    dst_file = find_arg(args, '-d', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/test_dst.txt')
    out_dir = find_arg(args, '-o', f'{os.path.dirname(os.path.abspath(__file__))}/out/merged')
    out_format = find_arg(args, '-f', 'json')

    try:
        os.makedirs(out_dir)
    except FileExistsError:
        pass
    finally:
        if out_format == 'json':
            merge_to_pairs_json(src_file, dst_file, out_dir)
        elif out_format == 'txt':
            merge_to_pairs_txt(src_file, dst_file, out_dir)


if __name__ == '__main__':
    main()
