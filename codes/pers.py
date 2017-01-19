import os
from flask import Flask, request, render_template, jsonify
import tweepy
import sys
import requests
import json,httplib,urllib
import csv
import pandas

consumer_key= '4F4rkhWlzJx1geKY7EIFoyOyp'
consumer_secret= '6uvr35kgy7CziY8zzGlHbywAVNEb8qzMaxs0DnL5lupH8HYH9D'
access_token='801128036364091392-3edsjInInkhwUR87PblYwKsuGmPsHob'
access_token_secret='KEL1QWcLZy1TsG4gloLB1w1wmme5Iu6b65wje5VubNjxM'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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
	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True)
	alltweets.extend(new_tweets)
	for tweet in alltweets:
	    thirtytweets.append(tweet.text.encode("utf-8"))
	thirtytweets = json.dumps(thirtytweets)
	#print thirtytweets
	r = requests.post('https://gateway.watsonplatform.net/personality-insights/api/v2/profile',auth=('14b0fbeb-89b2-4a04-a442-c6a21af1eed4','ec2MeIUi6SOY'),headers={'content-type': 'text/plain','accept': 'text/csv'},data=json.dumps(thirtytweets))
	print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
	pers_value = [[r.text.encode("utf-8")] for i in r]
	#print r.text

	
	with open('pers.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["personality"])
		writer.writerows(pers_value)
	pass
	
	data_pers = pandas.read_csv('pers.csv')
	#print(data_pers.columns)
	#colHH = data_pers['personality']
	k = data_pers.iloc[1].str.split(",")
	print k[0][49]
	
	print ("*******************************************************************************************************")




	

