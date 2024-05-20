import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
import pandas as pd

# 读取距离数据
def read_distance_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    documents = set()
    distances = []

    for line in lines:
        doc1, doc2, dist = line.strip().split()
        documents.add(doc1)
        documents.add(doc2)
        distances.append((doc1, doc2, float(dist)))

    documents = sorted(documents)
    doc_index = {doc: idx for idx, doc in enumerate(documents)}

    distance_matrix = np.zeros((len(documents), len(documents)))

    for doc1, doc2, dist in distances:
        idx1 = doc_index[doc1]
        idx2 = doc_index[doc2]
        distance_matrix[idx1, idx2] = dist
        distance_matrix[idx2, idx1] = dist  # 因为是对称的

    return documents, distance_matrix

# 主函数
def main():
    file_path = '../Similarity/distances/en.txt'
    documents, distance_matrix = read_distance_file(file_path)

    # 从控制台输入聚类数量k
    k = int(input("请输入聚类数量k: "))

    # 使用 k-means 算法
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    # 使用距离矩阵作为输入
    kmeans.fit(distance_matrix)
    labels = kmeans.labels_

    # 输出结果
    clusters = {}
    for idx, label in enumerate(labels):
        doc = documents[idx]
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(doc)

    for label, cluster_docs in clusters.items():
        print(f"\033[1;31m[Cluster {label}]\033[0m: {', '.join(cluster_docs)}")

if __name__ == "__main__":
    main()
