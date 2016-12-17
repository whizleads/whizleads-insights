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
	connection.request('GET', '/classes/Lead', '', {
	       "X-Parse-Application-Id": "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB",
	       "X-Parse-REST-API-Key": "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w"
	     })
	result = json.loads(connection.getresponse().read())
	print result

	return jsonify(result)

@app.route('/Insight')
def insight():

	connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
	connection.connect()
	connection.request('GET', '/classes/Insight', '', {
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
