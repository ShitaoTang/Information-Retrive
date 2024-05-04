from flask import Flask, render_template, request
from search import Search

app = Flask(__name__)
es = Search()

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/')
def search():
    query = request.form.get('query', '')
    return render_template("index.html", query=query, results = [], from_ = 0, total = 0)

@app.get('/document/<id>')
def get_documemnt(id):
    return 'Document not found'

@app.cli.command()
def reindex():
    '''Reindex all documents to Elasticsearch'''
    response = es.reindex()
    print(f'Index with {len(response["items"])} documents created in {response["took"]} ms.')