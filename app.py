import requests 
import json
from flask import Flask, render_template, request
import flask
import pystache
import os
import local as l

app = Flask(__name__)

keys = ['zipcode', 'dollarsobligated', 'fundingrequestingagencyid', 'effectivedate', 
        'contractactiontype', 'descriptionofcontractrequirement', 'vendorname', 'principalnaicscode',
        'city', 'state', 'productorservicecode', 'numberofemployees', 'unique_transaction_id']
LIMIT = 1000

base_url = 'https://spending-api.us/api/v1'
awards = '/awards'
query = '/?limit={}'.format(LIMIT)

# def process(result):
#     dictionary = {}
#     dictionary['meta'] = {}
#     num_results = len(result['results'])
#     dictionary['meta']['num_results'] = num_results
    
#     dictionary['results'] = []
#     for i in range(num_results):
#         agency = result['results'][i]['awarding_agency']['subtier_agency']['name']
#         recipient = result['results'][i]['recipient']['recipient_name']
        
#         dictionary['results'].append({'agency' : agency, 'recipient':recipient})
        
#     return {'processed':dictionary, 'raw':result}

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/local_file', methods = ['POST'])
def local():
    state = request.form['state-select']
    size = request.form['size']
    naics2 = request.form['naics2']
    naics4 = request.form['naics4']
    zipcode = request.form['zipcode-select']
    
    query = {}
    if not zipcode == "":
        query['zipcode'] = str(zipcode)
    if not naics4 == "Select":
        naics = int(naics4[0:4])
        query['principalnaicscode'] = str(naics)
    if not size == "Select":
        query['numberofemployees'] = str(size)
    if state == "CA":
        query['zipcode'] = "92101"

    data = l.filter_and_extract(query, keys, limit=1000)
    print data
    return render_template('dashboard.html', data=data)

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
    
    return flask.jsonify(result)

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)