import random
import re
import nltk.data

nltk.download('punkt')

accented_chars_vietnamese = [
    ['a', 'á', 'à', 'ả', 'ã', 'ạ', 'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ'],
    ['o', 'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ'],
    ['e', 'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ'],
    ['u', 'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự'],
    ['i', 'í', 'ì', 'ỉ', 'ĩ', 'ị'],
    ['y', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ'],
    ['d', 'đ'],
]

remove_accend_threshold = 0.85

accented_chars_vietnamese_all = []

for l in accented_chars_vietnamese:
    accented_chars_vietnamese_all += l


class VnUtils:
    def __init__(self, text):
        self.text = text
        return

    def tokenize(self, text):
        lines = self.split_sentences(text)
        return lines

    def make_noisy(self):
        clean_text = self.clean_text(self.text)
        lines = self.tokenize(clean_text)
        noisy_lines = []
        words = []
        noisy_words = []

        for line in lines:
            noisy = self.remomve_accend(line, remove_accend_threshold)
            noisy_lines.append(noisy)
            words += self.split_words(line)
            noisy_words += self.split_words(noisy)

        return lines, noisy_lines, words, noisy_words

    def remomve_accend(self, sentence, threshold):
        noisy_sentence = ''
        noisy_indies = []
        noisy_set = []

        for index, letter in enumerate(sentence):
            noisy = []
            for pre_set in accented_chars_vietnamese:
                for ch in pre_set:
                    if ch == letter:
                        noisy = pre_set
                        noisy_indies.append(index)

            noisy_set.append(noisy)

        for index, letter in enumerate(sentence):
            char = sentence[index]
            if len(noisy_set[index]) > 0 and random.random() < threshold:
                char_set = noisy_set[index]
                char = char_set[0]
            noisy_sentence += char

        return noisy_sentence

    def clean_text(self, text):
        text = re.sub(r'\n', ' ', text)
        text = re.sub('\.\.\.', ' ', text)
        text = re.sub('\.\..', ' ', text)
        text = re.sub('-', ' ', text)
        text = re.sub(':', '. ', text)
        text = re.sub('\!', '. ', text)
        text = re.sub('\?', '. ', text)
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
        text = re.sub(r'[{}@_*>()\\#%+=\[\]]', '', text)
        text = re.sub('a0', '', text)
        text = re.sub('\'92t', '\'t', text)
        text = re.sub('\'92s', '\'s', text)
        text = re.sub('\'92m', '\'m', text)
        text = re.sub('\'92ll', '\'ll', text)
        text = re.sub('\'91', ' ', text)
        text = re.sub('\'92', ' ', text)
        text = re.sub('\'93', ' ', text)
        text = re.sub('\'94', ' ', text)
        text = re.sub('\.', '. ', text)
        text = re.sub('\!', '! ', text)
        text = re.sub('\?', '? ', text)
        text = re.sub(' +', ' ', text)
        return text

    def split_sentences(self, text):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        lines = tokenizer.tokenize(text)
        return lines

    def split_words(self, sentence):
        tokenizer = nltk.tokenize
        words = tokenizer.word_tokenize(sentence)
        return words