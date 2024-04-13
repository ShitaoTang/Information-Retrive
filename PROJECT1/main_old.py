import os
import re
import zhconv
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

# 初始化词形还原器
lemmatizer = WordNetLemmatizer()

# import pynlpir

# pynlpir.open()

def get_character_cn(src_text):
    dest_text = re.sub(r"[^\u4e00-\u9fa5]+", '', src_text)
    # convert zh-tw/zh-hk/zh-hant to zh-cn
    dest_text = zhconv.convert(dest_text, "zh-cn")
    # using pynlpir to segment chinese text
    segments = pynlpir.segment(dest_text, pos_tagging = False)
    dest_text = ' '.join(segments)
    return dest_text

def get_character_en(src_text):
    dest_text = re.sub(r"[^A-Za-z]+", ' ', src_text)
    dest_text = dest_text.lower()
    return dest_text

def get_characterized_file(src_file, dest_file, get_character):
    with open(src_file, 'r', encoding = "utf-8") as f:
        dest_text = get_character(f.read())
    with open(dest_file, 'w', encoding = "utf-8") as f:
        f.write(dest_text)

dict_get_character = {
    "en": get_character_en,
    "cn": get_character_cn
}

def characterize(src_dir, dest_dir, type):
    os.makedirs(dest_dir, exist_ok = True)
    
    files = os.listdir(src_dir)
    index = 1
    for file in files:
        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, f"{index}.txt")
        # using dictionary to call function instead of "if...else..."
        get_characterized_file(src_file, dest_file, dict_get_character[type])
        index += 1


# # cn
# src_dir_cn = "downloaded/cn"
# dest_dir_cn = "res/cn"
# characterize(src_dir_cn, dest_dir_cn, "cn")

# #en
# src_dir_en = "downloaded/en"
# dest_dir_en = "res/en"
# characterize(src_dir_en, dest_dir_en, "en")

#delete stop-words
def delete(src_file, stopwords_list):
    with open(src_file, 'r', encoding = "utf-8") as f:
        src_text = f.read()
    words = src_text.split()
    dest_text = [word for word in words if word not in stopwords_list]
    return ' '.join(dest_text)

# with open('stopwords/cn.txt', 'r', encoding = "utf-8") as f:
#     stopwords_list = set(f.read().splitlines())
# text = delete_stopwords("seg/cn/2.txt", stopwords_list)
# print(text)

def delete_stopwords(src_dir, dest_dir, stopwords_list):
    os.makedirs(dest_dir, exist_ok = True)

    files = os.listdir(src_dir)
    index = 1
    for file in files:
        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, f"{index}.txt")
        deleted_text = delete(src_file, stopwords_list)
        with open(dest_file, 'w') as f:
            f.write(deleted_text)
        index += 1

# with open("stopwords/cn.txt", 'r', encoding = "utf-8") as f:
#     stopwords_list_cn = set(f.read().splitlines())
# delete_stopwords("seg/cn", "res/cn", stopwords_list_cn)

# with open("stopwords/en.txt", 'r', encoding = "utf-8") as f:
#     stopwords_list_en = set(f.read().splitlines())
# delete_stopwords("seg/en", "res/en", stopwords_list_en)

def porter_stemming(src_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok = True)

    files = os.listdir(src_dir)
    index = 1
    
    for file in files:
        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, f"{index}.txt")
        
        with open(src_file, 'r') as f:
            src_text = f.read()
        
        words = word_tokenize(src_text)
        pos_tags = pos_tag(words)

        dest_text = []
        for word, pos in pos_tags:
            item = lemmatizer.lemmatize(word, pos = pos[0].lower()) if pos[0].lower() in ['a', 'n', 'v'] else lemmatizer.lemmatize(word)
            dest_text.append(item)
        
        with open(dest_file, 'w') as f:
            f.write(' '.join(dest_text))

        index += 1

porter_stemming('res/en', 'final/en')
