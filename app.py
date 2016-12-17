import os
from flask import Flask, request, render_template, jsonify
import sys
import requests
import json,httplib

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/lead')
def lead():

connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
	connection.connect()
	connection.request('POST', '/classes/Insight', json.dumps({
       "user": 
			{
			  "__type": "Pointer",
			  "className": "_User",
			  "objectId": "suFefMagbS"
			},
       "lead":
       		{
			  "__type": "Pointer",
			  "className": "Lead",
			  "objectId": "DRzfTPRg4L"
			},
       "type": "topic",
       "confidence": 95,
       "tweet": "Bill Gates is coming to Australia",
       "insight": "Bill Gates"
     }), {
	       "X-Parse-Application-Id": "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB",
	       "X-Parse-REST-API-Key": "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w",
	       "Content-Type": "application/json"
	     })
	result = json.loads(connection.getresponse().read())
	print result

	return jsonify(result)

# TECH DEBT: We should be using a POST request using POSTMAN or similar.
# As we will use the API internally for the moment it is "acceptable"
@app.route('/insight')
def insight():

	connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
	connection.connect()
	# TECH DEBT: Keys should never store keys in the repository. 
	# We should be passing the keys in the request using POSTMAN or similar. 
	# As we are in Development Environment instead of Production Environment it is "acceptable"
	connection.request('GET', '/classes/Lead', '', {
	       "X-Parse-Application-Id": "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB",
	       "X-Parse-REST-API-Key": "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w"
	     })
	result = json.loads(connection.getresponse().read())
	print result

	return jsonify(result)

port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    app.run()
