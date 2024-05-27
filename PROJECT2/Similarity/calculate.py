import os
import math

def get_tf(document):
    tfs = {}
    terms = document.split()

    for term in terms:
        tfs[term] = tfs.get(term, 0) + 1
    
    for tf in tfs:
        tfs[tf] = 1 + math.log(tfs[tf])
    return tfs


def get_df(folder_path):
    dfs = {}
    terms = set()
    num_docs = 0
    
    # 先获取所有的词
    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", 'r') as f:
            terms.update(f.read().split())
            num_docs += 1

    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", 'r') as f:
            content = set(f.read().split())
        for term in terms:
            if term in content:
                dfs[term] = dfs.get(term, 0) + 1

    return dfs, num_docs


def get_idf(dfs, num_docs):
    idfs = {}

    for term, df in dfs.items():
        idfs[term] = math.log(num_docs / df)

    return idfs


def get_tfidfs(folder_path):
    dfs, num_docs = get_df(folder_path)
    idfs = get_idf(dfs, num_docs)
    tfidfs = {}

    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", 'r') as f:
            tf = get_tf(f.read())
            tfidf = {}
            for term, tf_value in tf.items():
                tfidf[term] = tf_value * idfs[term]
            tfidfs[filename] = tfidf

    return tfidfs


# for filename, tfidf in get_tfidfs("../docs/cn").items():
#     if not os.path.exists("tfidfs/cn"):
#         os.makedirs("tfidfs/cn")
#     with open(f"tfidfs/cn/{filename}", 'w') as f:
#         for term, value in tfidf.items():
#             f.write(f"{term} {value}\n")

# for filename, tfidf in get_tfidfs("../docs/en").items():
#     if not os.path.exists("tfidfs/en"):
#         os.makedirs("tfidfs/en")
#     with open(f"tfidfs/en/{filename}", 'w') as f:
#         for term, value in tfidf.items():
#             f.write(f"{term} {value}\n")

# 归一化
def normalize(folder_path):
    tf_idfs = get_tfidfs(folder_path)
    
    # 对tf_idfs的每一项的tfidf的value进行归一化：value除以所有value的平方和的开方
    for filename, tfidf in tf_idfs.items():
        sum_square = 0
        for value in tfidf.values():
            sum_square += value ** 2
        sum_square = math.sqrt(sum_square)
        for term in tfidf:
            tfidf[term] /= sum_square

    # 保存归一化后的tf_idfs到文件tfidfs_normalized
    if not os.path.exists(f"tfidfs_normalized/{folder_path.split('/')[-1]}"):
        os.makedirs(f"tfidfs_normalized/{folder_path.split('/')[-1]}")
    for filename, tfidf in tf_idfs.items():
        with open(f"tfidfs_normalized/{folder_path.split('/')[-1]}/{filename}", 'w') as f:
            for term, value in tfidf.items():
                f.write(f"{term} {value}\n")

    return tf_idfs

# 对任意两个文件计算cosine distance，步骤：分别用两个dict存储两个文件的term和对应的tfidf，如果term相同则计算两个tfidf的乘积，最后求和，如果term不同则乘积为0

# 对folder_path下的所有文件计算cosine distance，步骤：先获取所有文件的路径，然后两两计算cosine distance，类似冒泡排序的思路，计算所有文件的相似度，最后保存在一个文件里，文件格式为：文件1 文件2 相似度，每一个占一行
 
def cosine_distance(folder_path):
    tf_idfs = normalize(folder_path)
    files = list(tf_idfs.keys())
    distances = {}

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            file1 = files[i]
            file2 = files[j]
            tfidf1 = tf_idfs[file1]
            tfidf2 = tf_idfs[file2]
            distance = 0
            for term in tfidf1:
                if term in tfidf2:
                    distance += tfidf1[term] * tfidf2[term]
            distances[(file1, file2)] = distance

    if not os.path.exists("distances"):
        os.makedirs("distances")
    with open(f"distances/{folder_path.split('/')[-1]}.txt", 'w') as f:
        for (file1, file2), distance in distances.items():
            f.write(f"{file1} {file2} {distance}\n")

    return distances

print("cn or en: ")
type = input()
print("filename1: ")
filename1 = input()
print("filename2: ")
filename2 = input()

with open(f"distances/{type}.txt", 'r') as f:
    for line in f:
        file1, file2, distance = line.split()
        if (file1 == filename1 and file2 == filename2) or (file1 == filename2 and file2 == filename1):
            print(f"cosine distance: {distance}")
            # write these two files to a new file file1_file2.log
            with open(f"{filename1}_{filename2}.log", 'w') as log:
                log.write(f"cosine distance: {distance}\n")
                with open(f"../docs/{type}/{filename1}", 'r') as f1:
                    log.write(f"{filename1}:\n")
                    log.write(f1.read())
                with open(f"../docs/{type}/{filename2}", 'r') as f2:
                    log.write(f"\n{filename2}:\n")
                    log.write(f2.read())
            break

# if __name__ == "__main__":
#     cosine_distance("../docs/cn")
#     cosine_distance("../docs/en")