from flask import Flask, render_template, request
from html import escape
from search import Search

# Initialize the Flask application
app = Flask(__name__)
# Initialize the search object (assumed to be using Elasticsearch)
es = Search()

@app.get('/')
def index():
    '''
    Render the index page with a search form.
    Returns:
        Rendered index.html template.
    '''
    return render_template('index.html')


@app.post('/')
def search():
    '''
    Handle the search form submission, perform a search using the provided query,
    and render the index page with search results.
    Returns:
        Rendered index.html template with search results, query, and pagination information.
    '''
    query = request.form.get('query', '')  # Get the search query from the form
    from_ = int(request.form.get('from_', 0))  # Get the pagination offset
    # Perform the search with Elasticsearch
    results = es.search(
        query={
            'multi_match': {
                'query': query,
                'fields': ['title', 'content'],
                'fuzziness': 'AUTO'
            }
        }, size=10, from_=from_
    )
    # Render the index page with search results
    return render_template('index.html', results=results['hits']['hits'],
                           query=query, from_=from_,
                           total=results['hits']['total']['value'])


@app.cli.command()
def reindex():
    '''
    Reindex all documents to Elasticsearch.
    This function is executed via a command line interface (CLI) command.
    '''
    response = es.reindex()
    print(f'Index with {len(response["items"])} documents created in {response["took"]} ms.')
    

@app.get('/document/<id>')
def get_document(id):
    '''
    Retrieve and display a single document by its ID.
    Args:
        id (str): The ID of the document to retrieve.
    Returns:
        Rendered document.html template with the document's title and content.
    '''
    document = es.retrieve_document(id)  # Retrieve the document from Elasticsearch
    title = document['_source']['title']  # Extract the title
    paragraphs = document['_source']['content'].split('\n')  # Split content into paragraphs
    return render_template('document.html', title=title, paragraphs=paragraphs)
