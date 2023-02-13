import os
import sys
from dataset_translation.translating.aws import translate_dataset
from dataset_translation.translating.huggingface_model import translate_dataset_with_model
from dataset_translation.utils.args import find_arg


def main():
    args = sys.argv

    source_file = find_arg(args, '-s', f'{os.path.dirname(os.path.abspath(__file__))}/../test_sets/small_test.txt')
    target_dir = find_arg(args, '-d', f'{os.path.dirname(os.path.abspath(__file__))}/../out/translated')
    use_aws = '-a' in args
    use_huggingface = '-h' in args

    try:
        os.makedirs(target_dir)
    except FileExistsError:
        pass
    finally:
        if use_aws:
            translate_dataset(source_file, target_dir)
        if use_huggingface:
            translate_dataset_with_model(source_file, target_dir, "Helsinki-NLP/opus-mt-en-sv",
                                         "Helsinki-NLP/opus-mt-en-sv")


if __name__ == '__main__':
    main()
