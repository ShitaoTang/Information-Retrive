import os
import math

def get_tf(document):
    '''
    Compute term frequency (TF) for a document.
    Args:
        document (str): The content of the document.
    Returns:
        dict: A dictionary of terms with their corresponding TF values.
    '''
    tfs = {}
    terms = document.split()

    for term in terms:
        tfs[term] = tfs.get(term, 0) + 1
    
    for tf in tfs:
        tfs[tf] = 1 + math.log(tfs[tf])
    return tfs


def get_df(folder_path):
    '''
    Compute document frequency (DF) for terms in a collection of documents.
    Args:
        folder_path (str): The path to the folder containing documents.
    Returns:
        tuple: A dictionary of terms with their corresponding DF values, and the total number of documents.
    '''
    dfs = {}
    terms = set()
    num_docs = 0
    
    # First, collect all unique terms
    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", 'r') as f:
            terms.update(f.read().split())
            num_docs += 1

    # Compute DF for each term
    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", 'r') as f:
            content = set(f.read().split())
        for term in terms:
            if term in content:
                dfs[term] = dfs.get(term, 0) + 1

    return dfs, num_docs


def get_idf(dfs, num_docs):
    '''
    Compute inverse document frequency (IDF) for terms.
    Args:
        dfs (dict): A dictionary of terms with their corresponding DF values.
        num_docs (int): The total number of documents.
    Returns:
        dict: A dictionary of terms with their corresponding IDF values.
    '''
    idfs = {}

    for term, df in dfs.items():
        idfs[term] = math.log(num_docs / df)

    return idfs



def get_tfidfs(folder_path):
    '''
    Compute TF-IDF values for all documents in a folder.
    Args:
        folder_path (str): The path to the folder containing documents.
    Returns:
        dict: A dictionary with filenames as keys and TF-IDF dictionaries as values.
    '''
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


# Calculate and save TF-IDF values for Chinese documents
for filename, tfidf in get_tfidfs("../docs/cn").items():
    if not os.path.exists("tfidfs/cn"):
        os.makedirs("tfidfs/cn")
    with open(f"tfidfs/cn/{filename}", 'w') as f:
        for term, value in tfidf.items():
            f.write(f"{term} {value}\n")

# Calculate and save TF-IDF values for English documents
for filename, tfidf in get_tfidfs("../docs/en").items():
    if not os.path.exists("tfidfs/en"):
        os.makedirs("tfidfs/en")
    with open(f"tfidfs/en/{filename}", 'w') as f:
        for term, value in tfidf.items():
            f.write(f"{term} {value}\n")


def normalize(folder_path):
    '''
    Normalize TF-IDF values for all documents in a folder.
    Args:
        folder_path (str): The path to the folder containing documents.
    Returns:
        dict: A dictionary with filenames as keys and normalized TF-IDF dictionaries as values.
    '''
    tf_idfs = get_tfidfs(folder_path)
    
    # Normalize TF-IDF values
    for filename, tfidf in tf_idfs.items():
        sum_square = 0
        for value in tfidf.values():
            sum_square += value ** 2
        sum_square = math.sqrt(sum_square)
        for term in tfidf:
            tfidf[term] /= sum_square

    # Save normalized TF-IDF values to file
    if not os.path.exists(f"tfidfs_normalized/{folder_path.split('/')[-1]}"):
        os.makedirs(f"tfidfs_normalized/{folder_path.split('/')[-1]}")
    for filename, tfidf in tf_idfs.items():
        with open(f"tfidfs_normalized/{folder_path.split('/')[-1]}/{filename}", 'w') as f:
            for term, value in tfidf.items():
                f.write(f"{term} {value}\n")

    return tf_idfs


def cosine_distance(folder_path):
    '''
    Compute cosine distance between all pairs of documents in a folder.
    Args:
        folder_path (str): The path to the folder containing documents.
    Returns:
        dict: A dictionary with document pairs as keys and their cosine distance as values.
    '''
    tf_idfs = normalize(folder_path)
    files = list(tf_idfs.keys())
    distances = {}

    # Compute cosine distance for each pair of documents
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

    # Save distances to file
    if not os.path.exists("distances"):
        os.makedirs("distances")
    with open(f"distances/{folder_path.split('/')[-1]}.txt", 'w') as f:
        for (file1, file2), distance in distances.items():
            f.write(f"{file1} {file2} {distance}\n")

    return distances


def main():
    '''
    Main function to compute and display cosine distances between documents.
    '''
    cosine_distance("../docs/cn")
    cosine_distance("../docs/en")

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
                # Write these two files to a new log file
                with open(f"{filename1}_{filename2}.log", 'w') as log:
                    log.write(f"cosine distance: {distance}\n")
                    with open(f"../docs/{type}/{filename1}", 'r') as f1:
                        log.write(f"{filename1}:\n")
                        log.write(f1.read())
                    with open(f"../docs/{type}/{filename2}", 'r') as f2:
                        log.write(f"\n{filename2}:\n")
                        log.write(f2.read())
                break

if __name__ == "__main__":
    main()
