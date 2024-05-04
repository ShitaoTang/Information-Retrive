import json
from pprint import pprint
import os
import time

from elasticsearch import Elasticsearch


class Search:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")  
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def create_index(self):
        self.es.indices.delete(index = "documents", ignore_unavailable = True)
        self.es.indices.create(index = "documents")

    def insert_documents(self, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': 'documents'}})
            operations.append(document)
        return self.es.bulk(operations = operations)

    def reindex(self):
        self.create_index()
        documents = []
        path_cn = "../docs/cn"
        for filename in os.listdir(path_cn):
            with open(f"{path_cn}/{filename}", 'r') as file:
                document = {
                    'title': filename,
                    'content': file.read()
                }
                documents.append(document)

        path_en = "../docs/en"
        for filename in os.listdir(path_en):
            with open(f"{path_en}/{filename}", 'r') as file:
                document = {
                    'title': filename,
                    'content': file.read()
                }
                documents.append(document)

        return self.insert_documents(documents)