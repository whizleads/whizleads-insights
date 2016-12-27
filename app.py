import os
from flask import Flask, request, render_template, jsonify
import tweepy
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Word
import sys
import requests
import json,httplib,urllib

consumer_key= '4F4rkhWlzJx1geKY7EIFoyOyp'
consumer_secret= '6uvr35kgy7CziY8zzGlHbywAVNEb8qzMaxs0DnL5lupH8HYH9D'
access_token='801128036364091392-3edsjInInkhwUR87PblYwKsuGmPsHob'
access_token_secret='KEL1QWcLZy1TsG4gloLB1w1wmme5Iu6b65wje5VubNjxM'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/insights')
def tweets():

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

	for i in range(len(twitterURL)):
	    alltweets = []
	    new_tweets = api.user_timeline(screen_name =twitterURL[i],count=20)
	    alltweets.extend(new_tweets)
	    #oldest = alltweets[-1].id - 1
	    for tweet in new_tweets:
	        analysis = TextBlob(tweet.text, analyzer=NaiveBayesAnalyzer())
	        
		try:
    			interestTopic=analysis.noun_phrases[1]
		except IndexError:
    			interestTopic = 'null'
	        polarity = 'Positive'
	        if (analysis.sentiment.p_pos < 0.50):
	            polarity = 'Negative'
	        connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
	        connection.connect()
	        connection.request('POST', '/classes/Insight', json.dumps({
	               "user": 
	                    {
	                      "__type": "Pointer",
	                      "className": "_User",
	                      "objectId": userid[i]
	                    },
	               "lead":
	                    {
	                      "__type": "Pointer",
	                      "className": "Lead",
	                      "objectId": leadid[i]
	                    },
	               "type": "topic",
	               "confidence": analysis.sentiment.p_pos*100,
	               "tweet": tweet.text,
	               "insight": polarity,
	               "tweetId": tweet.id,
	               "interestTopic": interestTopic,
	               "description": "insight"
	             }), {
	                "X-Parse-Application-Id": "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB",
	                "X-Parse-REST-API-Key": "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w",
	                "Content-Type": "application/json"
	             })

	return ('Successfully added data to Insights!')


port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    app.run()

