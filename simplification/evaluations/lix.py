import os
import sys

sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}/../..')
from helpers.args import find_arg


def calc_lix(sequence):
    sentences = list(filter(lambda x : len(x) > 1, sequence.split('.')))
    S = len(sentences)
    W = 0
    L = 0
    for s in sentences:
        trimmed = ''.join(list(filter(lambda l : l.isalnum() or l == ' ', s)))
        for w in trimmed.split():
            W += 1
            if len(w) > 6:
                L += 1

    return W / S + (L * 100) / W


def evaluate_results(orig, simplified, out):
    orig = open(orig)
    simplified = open(simplified)
    out = open(out, 'w+')

    orig_line = orig.readline()
    simplified_line = simplified.readline()

    while orig_line and simplified_line:
        lix_orig = calc_lix(orig_line)
        lix_simp = calc_lix(simplified_line)
        diff = lix_simp - lix_orig

        out_line = f'{lix_orig},{lix_simp},{diff},{diff / lix_orig}\n'
        out.write(out_line)

        orig_line = orig.readline()
        simplified_line = simplified.readline()

    orig.close()
    simplified.close()
    out.close()


def main():
    args = sys.argv

    orig = find_arg(args, '-o', '')
    simplified = find_arg(args, '-s', '')
    simplified_file = simplified[simplified.rfind('/') + 1:]
    target_dir = find_arg(args, '-d', f'{os.path.dirname(os.path.abspath(__file__))}/../out/evaluation')
    out_file = f'{target_dir}/{simplified_file}.lix'

    try:
        os.makedirs(target_dir)
    except FileExistsError:
        pass
    finally:
        evaluate_results(orig, simplified, out_file)


if __name__ == '__main__':
    main()