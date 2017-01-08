import os
from flask import Flask, request, render_template, jsonify
import tweepy
import sys
import requests
import json,httplib,urllib
from google.cloud import language
#export GOOGLE_APPLICATION_CREDENTIALS="WhizLeadsInsights.json"

consumer_key= '4F4rkhWlzJx1geKY7EIFoyOyp'
consumer_secret= '6uvr35kgy7CziY8zzGlHbywAVNEb8qzMaxs0DnL5lupH8HYH9D'
access_token='801128036364091392-3edsjInInkhwUR87PblYwKsuGmPsHob'
access_token_secret='KEL1QWcLZy1TsG4gloLB1w1wmme5Iu6b65wje5VubNjxM'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = language.Client()

connection = httplib.HTTPSConnection('parseapi.back4app.com',443)
params = urllib.urlencode({
        "where":json.dumps({
       "manualTwitterURL": {
         "$ne": ""
       }
     }),
    "include":"user",
    "keys":"manualTwitterURL,user.objectId"
    })
connection.connect()
connection.request('GET', '/classes/Lead?%s' % params, '', {
       "X-Parse-Application-Id": "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB",
       "X-Parse-REST-API-Key": "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w"
     })
result = json.loads(connection.getresponse().read())

twitterURL = []
leadid=[]
userid = []
for i in range(0,len(result['results'])):
    twitterURL.append(result['results'][i]['manualTwitterURL'])
    leadid.append(result['results'][i]['objectId'])
    userid.append(result['results'][i]['user']['objectId'])
for i in range(0,len(twitterURL)):
	alltweets = []
	thirtytweets = []
	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=30, exclude_replies= True)
	alltweets.extend(new_tweets)
	for tweet in alltweets:
	    thirtytweets.append(tweet.text.encode("utf-8"))
	thirtytweets = json.dumps(thirtytweets)
	document = client.document_from_text(thirtytweets)
	entities = document.analyze_entities()
	
	for entity in entities:
		print('         name: %s' % (entity.name,))
		print('         type: %s' % (entity.entity_type,))
		print('     salience: %s' % (entity.salience,))
		print('=' * 20)
		break

	
