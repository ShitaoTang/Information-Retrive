import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
import pandas as pd

# Function to read the distance data from a file
def read_distance_file(file_path):
    '''
    Reads a file containing pairwise document distances and returns a sorted list of documents
    and a distance matrix.
    
    Args:
        file_path (str): The path to the file containing document distances.
    
    Returns:
        documents (list): A sorted list of unique document names.
        distance_matrix (numpy.ndarray): A symmetric matrix of distances between documents.
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    documents = set()  # Initialize an empty set to store document names
    distances = []  # Initialize an empty list to store distances

    # Parse each line to extract document pairs and their distances
    for line in lines:
        doc1, doc2, dist = line.strip().split()
        documents.add(doc1)
        documents.add(doc2)
        distances.append((doc1, doc2, float(dist)))

    # Sort the documents to ensure consistent indexing
    documents = sorted(documents)
    doc_index = {doc: idx for idx, doc in enumerate(documents)}

    # Initialize a zero matrix for the distance values
    distance_matrix = np.zeros((len(documents), len(documents)))

    # Fill the distance matrix with the parsed distance values
    for doc1, doc2, dist in distances:
        idx1 = doc_index[doc1]
        idx2 = doc_index[doc2]
        distance_matrix[idx1, idx2] = dist
        distance_matrix[idx2, idx1] = dist  # Symmetric matrix

    return documents, distance_matrix

# Main function to execute the clustering process
def main():
    '''
    Main function to read distance data, perform K-means clustering,
    and print the resulting clusters.
    
    Prompts the user to input the number of clusters.
    '''
    file_path = '../Similarity/distances/en.txt'  # Path to the distance file
    documents, distance_matrix = read_distance_file(file_path)

    # Input the number of clusters from the console
    k = int(input("Please enter the number of clusters k: "))

    # Initialize and fit the KMeans algorithm
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    
    # Fit the KMeans algorithm using the distance matrix
    kmeans.fit(distance_matrix)
    labels = kmeans.labels_

    # Organize documents into clusters based on their labels
    clusters = {}
    for idx, label in enumerate(labels):
        doc = documents[idx]
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(doc)

    # Output the clustered documents
    for label, cluster_docs in clusters.items():
        print(f"\033[1;31m[Cluster {label}]\033[0m: {', '.join(cluster_docs)}")

if __name__ == "__main__":
    main()
