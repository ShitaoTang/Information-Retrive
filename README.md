# Information Retrieve Course Projects

This repository contains projects for the Information Retrieval course. Each project directory (e.g., PROJECT1) represents a specific assignment.

~~Just as you read the name of this repository, it's "retrive" instead of "retrieve". We believe in embracing our typos and turning them into memorable moments~~

## Project1

Project1 focuses on implementing a download engine and preprocessing documents.

### Tasks

1. Implement a download engine to fetch at least 500 English and 500 Chinese documents/web pages.
2. Preprocess the downloaded documents automatically:
   - Tokenize words and perform characterization, including removing special characters and converting to lowercase.
   - Select and implement appropriate Chinese word segmentation techniques and tools.
   - Remove English and Chinese stop words.
   - Implement English Porter Stemming functionality.
   - Save the processed documents as simplified files for future indexing (e.g., News_1_E.txt for English documents, News_1_C.txt for Chinese documents).

### File Structure

```
Information Retrive
└── PROJECT1
    ├── Makefile        # Makefile for running scripts and tasks
    ├── crawl.py        # Script for crawling web pages
    ├── downloaded      # Directory for downloaded documents
    │   ├── cn
    │   └── en
    ├── main.py         # Main script for processing documents
    ├── main_old.py     # Old version of the main script
    ├── res             # Directory for processed documents
    │   ├── cn
    │   └── en
    ├── stopwords       # Directory for stop words
    │   ├── cn.txt
    │   └── en.txt
    └── test.py         # Script for testing functionalities
```

## Usage

### 1. Clone the Repository and Rename

First, clone this repository to your local machine and rename the folder to `IR_PROJECTS` (or any other preferred name), and change current directory:
```
git clone git@github.com:ShitaoTang/Information-Retrive.git
mv Information-Retrive IR_PROJECTS
cd IR_PROJECTS/PROJECT1
```

### 2. Optional: Delete the `downloaded` and `res`Folder

If desired, you can delete the `downloaded` and `res` folder:
```
rm -rf downloaded res
```

### 3. Install Dependencies

Make sure you have the required libraries installed. You can do this by running:
```
pip install beautifulsoup4 requests nltk pynlpir zhconv
```
After you install `pynlpir`, you may need to get a liscence by running this according to the [manual](https://pynlpir.readthedocs.io/en/latest/installation.html):
```
pynlpir update
```
If you have difficulty downloading a newest liscence， you can download it manually [here](https://github.com/NLPIR-team/NLPIR/blob/master/License/license%20for%20a%20month/NLPIR-ICTCLAS分词系统授权/NLPIR.user). Run this:
```
python -c "import site; print(site.getsitepackages()[0])"
```
You'll see a $path is printed, and put `NLPIR.user` under $path. You need to replace $path with the actual path printed in the terminal in the previous step.
```
mv NLPIR.user $path 
```

NLTK requires additional data modules to be downloaded in order to use certain functionalities. You can download these modules by running follwing command in your terminal:
```
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('snowball_data')"
```

### 4. Crawling and Running the Code
To initiate web crawling, first ensure that you have make installed on your computer. You can then run by running this(ensure you are under PROJECT1/, where the Makefile is located):
```
make crawl
```
Whether you can download all the web-pages depends on your network status (please ensure you can access Wikipedia at least). If failed, you can modify `Clawer_cn.start_url` in `main.py` to any other Chinese word's Wikipedia URL. Generally speaking, web-pages from ietf.org are generally accessible without network connection errors. At least I haven't had a 404 Not found.

This process may take between 3 to 10 minutes. **During this time, you might consider taking a short break and enjoying the scenery. Perhaps there's a gentle breeze, a beautiful sunset, or an evening glow waiting for you.**

After the crawling process is complete, you can see a new folder `downloaded/` is generated. Then running this to process the downloaded documents and web-pages:
```
make run
```
This step should complete quickly, typically within 30 seconds, depending on your computer's performance. Once the process is finished, you will notice a new res folder `res/` in the current directory. This folder contains the processed document files.

***

## Contributing

Contributions to this repository are welcome. If you have any suggestions or improvements, please feel free to open an issue or submit a pull request.


---


## Project2

Project2 focuses on implementing text search functionality, document similarity comparison, and document clustering.

### Tasks

1. **Establish and Implement Text Search Functionality**:
   - Utilize open-source search engines such as [Lucene](http://lucene.apache.org/), [ElasticSearch](https://www.elastic.co/cn/elasticsearch/), or [Lemur](http://www.lemurproject.org/). Review relevant documentation and install the necessary software.
   - Develop a search functionality for 500 preprocessed English and Chinese documents/web pages.
   - Index the documents using the chosen software. Then, using either a front-end interface or an existing interface, input keywords and display search results.
   - The front-end can display results in the form of a web page, application, or by using available interface tools.
   - Implement search capabilities for both English and Chinese documents.

2. **Document Similarity Comparison**:
   - Calculate the similarity between any two documents using Cosine Distance. List the original text of the documents and provide the similarity value.
   - Attempt to implement a program for detecting duplicate documents.

3. **Clustering of Downloaded Documents using K-Means**:
   - Use the K-Means clustering algorithm to cluster the 500 English/Chinese documents into 20 categories. Display the three largest clusters and the five most representative documents in each cluster (i.e., the documents closest to the cluster center).
   - Cluster the documents into different numbers of clusters, such as 5, 10, 25, and 50, and compare the differences and changes in the clustering results.
   - The distance for clustering can be calculated using either Cosine Distance or Euclidean Distance.

### File Structure

```
Information Retrive
├── PROJECT1
└── PROJECT2
    ├── Cluster
    │   └── kmeans.py          # Script implementing the K-Means clustering algorithm
    ├── Search
    │   ├── app.py             # Main script for flask application
    │   ├── requirements.txt   # Dependencies required for app.py and search.py
    │   ├── search.py          # Script for handling search functionality and indexing
    │   ├── static             
    │   └── templates          # Directory for HTML templates
    ├── Similarity
    │   ├── calculate.py       # Script for calculating document cosine distance
    │   ├── distances          # Directory for storing distance data
    │   │   ├── cn.txt        
    │   │   └── en.txt         
    │   ├── tfidfs             # Directory for storing TF-IDF data
    │   │   ├── cn
    │   │   └── en
    │   └── tfidfs_normalized  # Directory for storing normalized TF-IDF data
    │       ├── cn
    │       └── en
    └── docs                   # Directory for pre-processed documents
        ├── cn                 
        └── en 
```