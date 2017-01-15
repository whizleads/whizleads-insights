import os
from flask import Flask, request, render_template, jsonify
import tweepy
import sys
import requests
import json,httplib,urllib
from watson_developer_cloud import ToneAnalyzerV3


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'WhizLeadsInsights.json'
consumer_key= '4F4rkhWlzJx1geKY7EIFoyOyp'
consumer_secret= '6uvr35kgy7CziY8zzGlHbywAVNEb8qzMaxs0DnL5lupH8HYH9D'
access_token='801128036364091392-3edsjInInkhwUR87PblYwKsuGmPsHob'
access_token_secret='KEL1QWcLZy1TsG4gloLB1w1wmme5Iu6b65wje5VubNjxM'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
tone_analyzer = ToneAnalyzerV3(
   username='6cd057f4-b2a9-409c-b8d7-07c28329e449',
   password='4bpwH6CaLspp',
   version='2016-05-19')

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/tone')
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
	et_score = []
	lt_score = []
	st_score = []
	for i in range(0,len(result['results'])):
	    twitterURL.append(result['results'][i]['manualTwitterURL'])
	    leadid.append(result['results'][i]['objectId'])
	    userid.append(result['results'][i]['user']['objectId'])
	for i in range(0,len(twitterURL)):
		alltweets = []
    	huntweets = []
    	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True)
    	alltweets.extend(new_tweets)
    	for tweet in alltweets:
        	huntweets.append(tweet.text.encode("utf-8"))
    	huntweets = json.dumps(huntweets)

    	k =tone_analyzer.tone(text=huntweets,sentences=False)
    	s = k["document_tone"]["tone_categories"][0]["tones"]
    	emo_tone = k["document_tone"]["tone_categories"][0]["tones"]
    	lan_tone = k["document_tone"]["tone_categories"][1]["tones"]
    	soc_tone = k["document_tone"]["tone_categories"][2]["tones"]
    	for i in range (0,5):
    		et_score.append(emo_tone[0]["score"])
    	for i in range(0,3):
    		lt_score.append(lan_tone[0]["score"])
    	for i in range(0,5):
    		st_score.append(soc_tone[0]["score"])
    	connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
    	connection.connect()
    	connection.request('POST', '/classes/Tone', json.dumps({
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
		       	"text":huntweets,
		       	"emotion_anger":et_score[0],
	       		"emotion_disgust":et_score[1],
	       		"emotion_fear":et_score[2],
	       		"emotion_joy":et_score[3],
	       		"emotion_sadness":et_score[4],
	       		"language_analytical":lt_score[0],
	       		"language_confident":lt_score[1],
	       		"language_tentative":lt_score[2],
	       		"social_openness":st_score[0],
	       		"social_conscientiousness":st_score[1],
	       		"social_extraversion":st_score[2],
	       		"social_agreeableness":st_score[3],
	       		"social_emotional_range":st_score[4],
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

