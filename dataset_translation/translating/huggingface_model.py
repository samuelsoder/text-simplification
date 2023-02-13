import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dataset_translation.utils.progress_bar import print_progress_bar


def translate_sentence_with_model(tokenizer, model, sentence):
    input_ids = tokenizer(sentence, return_tensors="pt").input_ids
    output = model.generate(input_ids, max_length=512)

    return tokenizer.decode(output[0], skip_special_tokens=True)


def translate_dataset_with_model(source_file: str, target_dir: str, tokenizer: str, model: str):
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
            target_file.write(f'{translate_sentence_with_model(tokenizer, model, line)}\n')
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
