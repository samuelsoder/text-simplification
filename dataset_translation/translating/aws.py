import time
import boto3
from botocore.client import BaseClient
from dataset_translation.helpers.progress_bar import print_progress_bar


def translate_sentence(sentence, translator: BaseClient):
    result = translator.translate_text(Text=sentence, SourceLanguageCode="en", TargetLanguageCode="sv")
    return result.get('TranslatedText')


def translate_dataset(source_file: str, target_dir: str):
    print("Setting up session")
    session = boto3.Session(profile_name="ilt-staging-admin")
    translator = session.client(service_name="translate", region_name="eu-central-1")

    start_time = time.time()
    translation_time = 0
    no_lines = 0
    total_lines = 15

    target_file = open(f'{target_dir}/aws-sv-translated.txt', 'w')

    print('---- Starting translation through AWS ----')
    print(f'Total number of sentences to translate: {total_lines}')
    print_progress_bar(no_lines, total_lines, 'Translating languages...')

    with open(source_file) as file:
        while True:
            sentence_time = time.time()
            line = file.readline()
            if len(line) == 0:
                break
            target_file.write(f'{translate_sentence(line, translator)}')
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