import argparse
import codecs
import os
import random
import traceback
from os import path

from .import vn_utils
from . import epub2txt
import os, shutil


def add_arguments(parser):
  """Build ArgumentParser."""
  parser.register("type", "bool", lambda v: v.lower() == "true")

  parser.add_argument("--src", type=str, default='ko', help="source language")
  parser.add_argument("--tgt", type=str, default='co', help="target language")
  parser.add_argument("--books_dir", type=str, default='./vnsc/books', help="books directory.")
  parser.add_argument("--data_dir", type=str, default='./vnsc/data', help="data directory.")
  parser.add_argument("--num_test", type=int, default=1, help="number of book use validation test")
  parser.add_argument("--num_dev", type=int, default=1, help="number of book use pre train test")


def clear_data(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def main(flags):
    book_path = flags.books_dir
    data_path = flags.data_dir

    clear_data(data_path)

    book_files = [f for f in os.listdir(book_path) if path.isfile(path.join(book_path, f))]
    book_devs = random.sample(range(0, len(book_files)), flags.num_dev)
    book_test = random.sample(range(0, len(book_files)), flags.num_test)

    total_train = 0
    total_dev = 0
    total_test = 0
    total_sentences = 0
    total_words = 0
    total_book = 0

    while len(list(set(book_devs) & set(book_test))) > 0:
        book_test = random.sample(range(0, len(book_files)), flags.num_test)

    for index, book in enumerate(book_files):
        try:
            data_type = 'train'
            total_book += 1

            if index in book_devs:
                data_type = 'dev'
                total_dev += 1

            if index in book_test:
                data_type = 'test'
                total_test += 1

            if data_type == 'train':
                total_train += 1


            src_file = '{}.{}'.format(data_type, flags.src)
            tgt_file = '{}.{}'.format(data_type, flags.tgt)

            converter = epub2txt.epub2txt(path.join(book_path, book))
            print("converting: {} ".format(converter.epub))
            content = converter.convert()
            cleaner = vn_utils.VnUtils(content)
            (lines, noisies, words, nosy_words) = cleaner.make_noisy()

            total_sentences += len(lines)
            total_words += len(words)

            with open(path.join(flags.data_dir, src_file), 'ab') as train_src_file:
                train_src_file.write(('\n').join(noisies).encode('utf-8'))
                train_src_file.close()

            with open(path.join(flags.data_dir, tgt_file), 'ab') as train_tgt_file:
                train_tgt_file.write('\n'.join(lines).encode('utf-8'))
                train_tgt_file.close()

            with open(path.join(flags.data_dir, 'vocab.{}'.format(flags.src)), 'ab') as vocab_src_file:
                vocab_src_file.write('\n'.join(nosy_words).encode('utf-8'))
                vocab_src_file.close()

            with open(path.join(flags.data_dir, 'vocab.{}'.format(flags.tgt)), 'ab') as vocab_tgt_file:
                vocab_tgt_file.write('\n'.join(words).encode('utf-8'))
                vocab_tgt_file.close()

            print("convert completed {} sentences of {}".format(len(lines), book))
        except Exception:
            print('convert failed')
            traceback.print_exc()

    print('convert done:')
    print('- total books: {}'.format(total_book));
    print('- dev books: {}'.format(total_dev));
    print('- test books: {}'.format(total_test));
    print('- total sentences: {}'.format(total_sentences));
    print('- total words: {}'.format(total_words));


if __name__ == "__main__":
    vnsc_parser = argparse.ArgumentParser()
    add_arguments(vnsc_parser)
    FLAGS, unparsed = vnsc_parser.parse_known_args()
    main(FLAGS)

