from pprint import pprint
import os
from elasticsearch import Elasticsearch

class Search:
    def __init__(self):
        '''
        Initialize the Search class by connecting to Elasticsearch.
        Prints information about the connected Elasticsearch client.
        '''
        self.es = Elasticsearch("http://localhost:9200")  
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)


    def create_index(self):
        '''
        Create the "documents" index in Elasticsearch, deleting it first if it already exists.
        '''
        self.es.indices.delete(index="documents", ignore_unavailable=True)
        self.es.indices.create(index="documents")


    def insert_documents(self, documents):
        '''
        Insert a list of documents into the "documents" index in bulk.
        Args:
            documents (list): A list of documents to insert into the index.
        Returns:
            dict: The response from the bulk insert operation.
        '''
        operations = []
        for document in documents:
            operations.append({'index': {'_index': 'documents'}})
            operations.append(document)
        return self.es.bulk(operations=operations)
    

    def reindex(self):
        '''
        Reindex all documents by creating the index and inserting documents from specified directories.
        Returns:
            dict: The response from the bulk insert operation.
        '''
        self.create_index()
        documents = []
        
        # Load Chinese documents from the specified directory
        path_cn = "../docs/cn"
        for filename in os.listdir(path_cn):
            with open(f"{path_cn}/{filename}", 'r') as file:
                document = {
                    'title': 'cn_' + filename,
                    'content': file.read()
                }
                documents.append(document)

        # Load English documents from the specified directory
        path_en = "../docs/en"
        for filename in os.listdir(path_en):
            with open(f"{path_en}/{filename}", 'r') as file:
                document = {
                    'title': 'en_' + filename,
                    'content': file.read()
                }
                documents.append(document)

        return self.insert_documents(documents)
    

    def search(self, **query_args):
        '''
        Perform a search query on the "documents" index.
        Args:
            query_args (dict): The query parameters for the search.
        Returns:
            dict: The search results from Elasticsearch.
        '''
        return self.es.search(index="documents", **query_args)
    

    def retrieve_document(self, id):
        '''
        Retrieve a document by its ID from the "documents" index.
        Args:
            id (str): The ID of the document to retrieve.
        Returns:
            dict: The retrieved document from Elasticsearch.
        '''
        return self.es.get(index="documents", id=id)
