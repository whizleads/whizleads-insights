import os
from flask import Flask, request, render_template, jsonify
import tweepy
from textblob import TextBlob
import sys
import requests
import json
from monkeylearn import MonkeyLearn

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
	}

	screen_name=[]
	leaduserid = []
	userid = []
	result = requests.get('https://parseapi.back4app.com/classes/Lead', headers=headers)
	r=json.loads(result.text)

'''	
	for i in range(0,len(r["results"])):
	    screen_name.append(r["results"][i]["manualTwitterURL"])
	    leaduserid.append(r["results"][i]['objectId'])
	for i in range(0,len("manualTwitterURL")):
	    userid.append(r["results"][i]['user']['objectId'])
	for i in range(len(screen_name)):
		alltweets = []
		new_tweets = api.user_timeline(screen_name =screen_name[i],count=20)
		alltweets.extend(new_tweets)
		#oldest = alltweets[-1].id - 1
		#new_tweets = api.user_timeline(screen_name = screen_name,count=20,since_id=oldest)
		ml = MonkeyLearn('ab32ac89200b6ee22560dd777fffc5d71457ee54')
   		for tweet in new_tweets:
       			text_list = [tweet.text]
       			tweetId= tweet.id
       			module_id = 'cl_8WSAPAph'
       			res = ml.classifiers.classify(module_id, text_list, sandbox=True)
       			x= res.result
        		confidence = 0.501 #as for now every time same value comes out
       			data = '{"type":"Sentiments","descriptions": text_list, "tweetId": tweetId, "Confidence": confidence,"user": userid[i],"lead":leaduserid[i] }'
       			response = requests.post('https://parseapi.back4app.com/classes/Insight', headers=headers, data=data)
'''
	return jsonify({'Successfully added data to Insights'})


port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    app.run()
