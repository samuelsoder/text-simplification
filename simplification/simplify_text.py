import time
import os
import sys

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}/..')
from helpers.progress_bar import print_progress_bar
from helpers.args import find_arg


class Simplifier:

    def __init__(self, path_to_model):
        self.model = AutoModelForSeq2SeqLM.from_pretrained(path_to_model)
        self.tokenizer = AutoTokenizer.from_pretrained(path_to_model)

    def simplify_sequence(self, sequence):
        encoded = self.tokenizer.encode(sequence, return_tensors='pt')
        output = self.model.generate(encoded, max_length=250)
        return self.tokenizer.decode(output[0])


def simplify_sequences(simplifier, sequences):
    out = []
    for s in sequences:
        out.append(simplifier.simplify_sequence(s))
    return out


def simplify_fully(simplifier, sequence):
    latest_res = ""
    times_simplified = 0
    while latest_res != sequence and times_simplified < 10:
        latest_res = sequence
        sequence = simplifier.simplify_sequence(sequence)
        times_simplified += 1
    return sequence


def simplify(path_to_model, source, target_dir, fully=False):
    simplifier = Simplifier(path_to_model)

    start_time = time.time()
    translation_time = 0
    no_lines = 0
    total_lines = sum(1 for _ in open(source))

    out_name = f'{source[source.rfind("/"):]}.simplified{".fully" if fully else ""}'
    out_file = f'{target_dir}/{out_name}'
    target = open(out_file, 'w+')

    print('---- Starting simplification ----')
    print(f'Total number of sentences to simplify: {total_lines}')
    print_progress_bar(no_lines, total_lines, 'Simplifying...')

    with open(source) as source_file:
        line = source_file.readline()
        while line:
            sequence_time = time.time()
            simplified = simplifier.simplify_sequence(line) if not fully else simplify_fully(simplifier, line)
            target.write(f'{simplified[8:-4]}\n')
            no_lines += 1
            translation_time += time.time() - sequence_time
            if no_lines % 10 == 0:
                print_progress_bar(no_lines, total_lines,
                                   prefix='Simplifying...',
                                   suffix=f'nb sequences done: {no_lines}, avg time per: {translation_time / no_lines}')
            line = source_file.readline()


    result_file = open(f'{target_dir}/results', 'w')
    result_file.write(f'Lines simplified: {no_lines} \n')
    result_file.write(f'Time taken: {time.time() - start_time} seconds\n')
    result_file.write(f'Average time per sequence: {translation_time / no_lines} seconds\n')
    result_file.close()


def main():
    args = sys.argv

    path_to_model = find_arg(args, '-m', '')
    source_file = find_arg(args, '-s', f'{os.path.dirname(os.path.abspath(__file__))}/test_sets/test.txt')
    target_dir = find_arg(args, '-d', f'{os.path.dirname(os.path.abspath(__file__))}/out/simplified')
    fully = '-f' in args

    try:
        os.makedirs(target_dir)
    except FileExistsError:
        pass
    finally:
        simplify(path_to_model, source_file, target_dir, fully)


def test():
    s = "Rymdfarkosten har två huvudelement : NASA Cassini - orbiter, uppkallad efter den italiensk - franska astronomen Giovanni Domenico Cassini, och ESA Huygens - sonden, uppkallad efter den holländska astronomen,"


if __name__ == '__main__':
    test()
