import os
import math
import re
import zhconv
# import pynlpir
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

# initialize the NLPIR segmenter
# pynlpir.open()

# initialize the poter_stemmer 
poter_stemmer = SnowballStemmer(language='english')

def get_tf(document):
    tfs = {}
    terms = document.split()

    for term in terms:
        tfs[term] = tfs.get(term, 0) + 1
    
    for tf in tfs:
        tfs[tf] = 1 + math.log(tfs[tf])
    return tfs


# 对文档的tf进行归一化，每个词的tf值除以文档中所有词的tf值的平方和
def normalize_tf(tf):
    norm = 0
    for term, tf_value in tf.items():
        norm += tf_value ** 2
    norm = math.sqrt(norm)
    for term in tf:
        tf[term] /= norm
    return tf


def get_similarity(tf, folder_path):

    max_similarity = 0
    max_filename = ""
    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", 'r') as f:
            tfidf = {}
            for line in f:
                term, tfidf_value = line.split()
                tfidf[term] = float(tfidf_value)
        # 已经获取了当前文档的tfidf
        similarity = 0
        for term in tf:
            if term in tfidf:
                tfidf[term] *= tf[term]
                similarity += tfidf[term]
        if similarity > max_similarity:
            max_similarity = similarity
            max_filename = filename
    return max_filename, max_similarity

def duplicate_check(document, folder_path):
    tf = get_tf(document)
    tf = normalize_tf(tf)
    return get_similarity(tf, folder_path)


def preprocess_cn(document):
    # read stopwords from file
    with open("../../PROJECT1/stopwords/cn.txt", 'r', encoding = "utf-8") as f:
        stopwords_list_cn = set(f.read().splitlines())

    extracted_chinese_text = re.sub(r"[^\u4e00-\u9fa5]+", '', document)

    simplified_chinese_text = zhconv.convert(extracted_chinese_text, "zh-cn")

    # segment Chinese text
    segments = pynlpir.segment(simplified_chinese_text, pos_tagging = False)
    segmented_text = ' '.join(segments)

    # remove stopwords
    words = segmented_text.split()
    filtered_words = [word for word in words if word not in stopwords_list_cn] 
    filtered_text= ' '.join(filtered_words)

    return filtered_text


def preprocess_en(document):
    with open("../../PROJECT1/stopwords/en.txt", 'r', encoding = "utf-8") as f:
        stopwords_list_en = set(f.read().splitlines())

    extracted_english_text = re.sub(r"[^A-Za-z]+", ' ', document)
    # lower all the letters
    lowered_text = extracted_english_text.lower()
    
    # remove stopwords
    words = lowered_text.split()
    filtered_words = [word for word in words if word not in stopwords_list_en]
    filtered_text = ' '.join(filtered_words)

    # porter stemming
    words = word_tokenize(filtered_text)
    stemmed_text = ' '.join(poter_stemmer.stem(word) for word in words)

    return stemmed_text


# 从文件中读取文档内容
with open('sample.txt', 'r', encoding='utf-8') as file:
    document = file.read()

    # 判断文档是中文还是英文
    if re.search(r'[\u4e00-\u9fa5]', document):
        document = preprocess_cn(document)
        max_filename, max_similarity = duplicate_check(document, "tfidfs_normalized/cn")
        print(f"Duplicate of document in Chinese: {max_filename} with similarity {max_similarity}")
    else:
        document = preprocess_en(document)
        max_filename, max_similarity = duplicate_check(document, "tfidfs_normalized/en")
        print(f"Duplicate of document in English: {max_filename} with similarity {max_similarity}")

# # 进行重复检查
# max_filename1, max_similarity1 = duplicate_check(document, "tfidfs_normalized/cn")
# max_filename2, max_similarity2 = duplicate_check(document, "tfidfs_normalized/en")

# # 比较相似度并输出结果
# if max_similarity1 > max_similarity2:
#     print(f"Duplicate of document in Chinese: {max_filename1} with similarity {max_similarity1}")
# else:
#     print(f"Duplicate of document in English: {max_filename2} with similarity {max_similarity2}")