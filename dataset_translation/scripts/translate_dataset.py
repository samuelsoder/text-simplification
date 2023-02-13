import os
import sys
from dataset_translation.translating.aws import translate_dataset
from dataset_translation.translating.huggingface_model import translate_dataset_with_model
from dataset_translation.utils.args import try_arg


def main():
    args = sys.argv

    source_file = try_arg(args, 1, f'{os.path.dirname(os.path.abspath(__file__))}/../test_sets/small_test.txt')
    target_dir = try_arg(args, 2, f'{os.path.dirname(os.path.abspath(__file__))}/../out/translated')

    try:
        os.makedirs(target_dir)
    except FileExistsError:
        pass
    finally:
        translate_dataset_with_model(source_file, target_dir, "Helsinki-NLP/opus-mt-en-sv", "Helsinki-NLP/opus-mt-en-sv")
        translate_dataset(source_file, target_dir)


if __name__ == '__main__':
    main()
