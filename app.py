import os
from flask import Flask, request, render_template, jsonify
import tweepy
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Word
import sys
import requests
import json

app = Flask(__name__)

consumer_key= '4F4rkhWlzJx1geKY7EIFoyOyp'
consumer_secret= '6uvr35kgy7CziY8zzGlHbywAVNEb8qzMaxs0DnL5lupH8HYH9D'
access_token='801128036364091392-3edsjInInkhwUR87PblYwKsuGmPsHob'
access_token_secret='KEL1QWcLZy1TsG4gloLB1w1wmme5Iu6b65wje5VubNjxM'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/lead')
def lead():
	
	headers = {
	    'X-Parse-Application-Id': '9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB',
	    'X-Parse-REST-API-Key': '6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w',
	    'Content-Type': 'application/json',
	}

	screen_name=[]
	userid = []
	leadid = []
	result = requests.get('https://parseapi.back4app.com/classes/Lead', headers=headers)
	r=json.loads(result.text)
	for i in range(0,len(r["results"])):
	    screen_name.append(r["results"][i]["manualTwitterURL"])
	    leadid.append(r["results"][i]["objectId"])
	for i in range(len(screen_name)):
	    alltweets = []
	    new_tweets = api.user_timeline(screen_name =screen_name[i],count=20)
	    alltweets.extend(new_tweets)
	    #oldest = alltweets[-1].id - 1
	    for tweet in new_tweets:
	        analysis = TextBlob(tweet.text, analyzer=NaiveBayesAnalyzer())
	        polarity = 'Positive'
	        if (analysis.sentiment.p_pos < 0.50):
	            polarity = 'Negative'
	        print ("Type : Sentiment Analysis and Topic of Interest")
	        print ("Description : Insight")
	        print ("Lead Id : ", leadid[i])
	        print ("Tweet : ",tweet.text)
	        print ("Tweet id : ",tweet.id)
	        print ("Insight Sentiment:",polarity)
	        print ("Confidence :  Positive score: " ,analysis.sentiment.p_pos*100, "  Negative score: ", analysis.sentiment.p_neg*100 )
	        print ("Areas of interest: ", analysis.noun_phrases)
	        print "---------------------------------------------------------------------------"
	        
	return jsonify({'Successfully added data to Insights'})


port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    app.run()
