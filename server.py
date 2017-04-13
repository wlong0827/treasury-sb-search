import requests 
import json
from flask import Flask, render_template, request
import flask
import pystache

app = Flask(__name__)

LIMIT = 100

base_url = 'https://spending-api.us/api/v1'
awards = '/awards'
query = '/?limit={}'.format(LIMIT)

def process(result):
    dictionary = {}
    dictionary['meta'] = {}
    num_results = len(result['results'])
    dictionary['meta']['num_results'] = num_results
    
    dictionary['results'] = []
    for i in range(num_results):
        agency = result['results'][i]['awarding_agency']['subtier_agency']['name']
        recipient = result['results'][i]['recipient']['recipient_name']
        
        dictionary['results'].append({'agency' : agency, 'recipient':recipient})
        
    return {'processed':dictionary, 'raw':result}

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/my-link', methods = ['POST'])
def my_link():
    location = request.form['location_id']
    url = base_url + awards + query + '&place_of_performance={}'.format(location)
    
    print "Requesting URL {}".format(url)

    response = requests.get(url)
    result = response.json()
    
    award_id = result['results'][0]['id']
    print award_id
    
    url = base_url + awards + '/{}'.format(award_id)
    
    response = requests.get(url)
    result = response.json()
#    result = process(result)
    
    return flask.jsonify(result)

if __name__ == '__main__':
  app.run(debug=True)