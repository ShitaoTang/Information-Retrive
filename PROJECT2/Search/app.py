from flask import Flask, render_template, request
from html import escape
from search import Search

app = Flask(__name__)
es = Search()

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/')
def search():
    query = request.form.get('query', '')
    from_ = int(request.form.get('from_', 0))
    results = es.search(
        query={
            'multi_match': {
                'query': query,
                'fields': ['title', 'content'],
                'fuzziness': 'AUTO'
            }
        }, size = 10, from_ = from_
    )
    return render_template('index.html', results = results['hits']['hits'],
                           query = query, from_ = from_,
                           total = results['hits']['total']['value'])


@app.cli.command()
def reindex():
    '''Reindex all documents to Elasticsearch'''
    response = es.reindex()
    print(f'Index with {len(response["items"])} documents created in {response["took"]} ms.')

@app.get('/document/<id>')
def get_document(id):
    document = es.retrieve_document(id)
    title = document['_source']['title']
    paragraphs = document['_source']['content'].split('\n')
    return render_template('document.html', title=title, paragraphs=paragraphs)
