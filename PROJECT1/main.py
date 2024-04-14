import os
import re
import zhconv
import pynlpir
import threading
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

# initialize the NLPIR segmenter
pynlpir.open()

# initialize the poter_stemmer 
poter_stemmer = SnowballStemmer(language='english')


def process_cn(src_dir, dest_dir):
    '''
    A function to process Chinese webpages:
    - Extract Chinese characters.
    - Convert traditional Chinese characters to simplified Chinese characters.
    - Segment Chinese text.
    - Remove stopwords.
    - Name and save the processed files according to its index.
    
    Args:
    - src_dir: Path to the folder containing the downloaded Chinese webpages.
    - dest_dir: Path to the folder where the processed files will be saved.
    '''
    
    os.makedirs(dest_dir, exist_ok = True)

    # read stopwords from file
    with open("stopwords/cn.txt", 'r', encoding = "utf-8") as f:
        stopwords_list_cn = set(f.read().splitlines())

    files = os.listdir(src_dir)
    index = 1
    for file in files:
        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, f"{index}.txt")
        
        with open(src_file, 'r', encoding = 'utf-8') as f:
            src_text = f.read()

        extracted_chinese_text = re.sub(r"[^\u4e00-\u9fa5]+", '', src_text)

        # convert zh-tw/zh-hk/zh-hant to zh-cn
        simplified_chinese_text = zhconv.convert(extracted_chinese_text, "zh-cn")

        # segment Chinese text
        segments = pynlpir.segment(simplified_chinese_text, pos_tagging = False)
        segmented_text = ' '.join(segments)

        # remove stopwords
        words = segmented_text.split()
        filtered_words = [word for word in words if word not in stopwords_list_cn] 
        filtered_text= ' '.join(filtered_words)

        with open(dest_file, 'w', encoding = "utf-8") as f:
            f.write(filtered_text)

        index += 1


def process_en(src_dir, dest_dir):
    '''
    A function to process English webpages:
    - Extract English words.
    - Lowercase all the letters.
    - Remove stopwords.
    - Stem English words.
    - Name and save the processed files according to its index.

    Args:
    - src_dir: Path to the folder containing the downloaded English webpages.
    - dest_dir: Path to the folder where the processed files will be saved.
    '''

    os.makedirs(dest_dir, exist_ok = True)

    with open("stopwords/en.txt", 'r', encoding = "utf-8") as f:
        stopwords_list_en = set(f.read().splitlines())

    files = os.listdir(src_dir)
    index = 1
    for file in files:
        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, f"{index}.txt")

        with open(src_file, 'r', encoding = "utf-8") as f:
            src_text = f.read()

        extracted_english_text = re.sub(r"[^A-Za-z]+", ' ', src_text)
        # lower all the letters
        lowered_text = extracted_english_text.lower()
        
        # remove stopwords
        words = lowered_text.split()
        filtered_words = [word for word in words if word not in stopwords_list_en]
        filtered_text = ' '.join(filtered_words)

        # porter stemming
        words = word_tokenize(filtered_text)
        stemmed_text = ' '.join(poter_stemmer.stem(word) for word in words)

        with open(dest_file, 'w', encoding = "utf-8") as f:
            f.write(stemmed_text)

        index += 1


def main():
   thread_cn = threading.Thread(target = process_cn, args = ("downloaded/cn", "res/cn"))
   thread_en = threading.Thread(target = process_en, args = ("downloaded/en", "res/en"))

   thread_cn.start()
   thread_en.start()

   thread_cn.join()
   thread_en.join()

if __name__ == "__main__":
    main()
