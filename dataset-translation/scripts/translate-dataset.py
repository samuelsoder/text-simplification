import os
import sys
import time

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end, flush=True)
    # Print New Line on Complete
    if iteration == total:
        print()


def try_arg(args, index, default):
    try:
        val = args[index]
    except IndexError:
        val = default
    return val


def translate_sentence(tokenizer, model, sentence):
    input_ids = tokenizer(sentence, return_tensors="pt").input_ids
    output = model.generate(input_ids, max_length=512)

    return tokenizer.decode(output[0], skip_special_tokens=True)


def translate_dataset(source_file: str, target_dir: str, tokenizer: str, model: str):
    print(f'Getting tokenizer: {tokenizer}', end='')
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)

    print(f'... done! \nGetting model: {model}', end='')
    model = AutoModelForSeq2SeqLM.from_pretrained(model)
    print('... done!')

    start_time = time.time()
    translation_time = 0
    no_lines = 0
    total_lines = 15

    target_file = open(f'{target_dir}/sv-translated.txt', 'w')

    print('---- Starting translation ----')
    print(f'Total number of sentences to translate: {total_lines}')
    print_progress_bar(no_lines, total_lines, 'Translating languages...')
    with open(source_file) as file:
        while True:
            sentence_time = time.time()
            line = file.readline()
            if len(line) == 0:
                break
            target_file.write(f'{translate_sentence(tokenizer, model, line)}\n')
            no_lines += 1
            translation_time += time.time() - sentence_time
            print_progress_bar(no_lines, total_lines,
                               prefix='Translating... ',
                               suffix=f'nb sentences done: {no_lines}, avg time per: {translation_time / no_lines}')

    result_file = open(f'{target_dir}/results', 'w')
    result_file.write(f'Lines translated: {no_lines} \n')
    result_file.write(f'Time taken: {time.time() - start_time} seconds\n')
    result_file.write(f'Average time per sentence: {translation_time / no_lines} seconds\n')
    result_file.close()


def main():
    args = sys.argv

    tokenizer = "Helsinki-NLP/opus-mt-en-sv"
    model = "Helsinki-NLP/opus-mt-en-sv"

    source_file = try_arg(args, 1, f'{os.path.dirname(os.path.abspath(__file__))}/../test_sets/small_test.txt')
    target_dir = try_arg(args, 2, f'{os.path.dirname(os.path.abspath(__file__))}/../out/translated')

    try:
        os.makedirs(target_dir)
    except FileExistsError:
        pass
    finally:
        translate_dataset(source_file, target_dir, tokenizer, model)


if __name__ == '__main__':
    main()
