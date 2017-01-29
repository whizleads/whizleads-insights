import os
from flask import Flask, request, render_template, jsonify
import tweepy
import sys
import requests
import json,httplib,urllib
from watson_developer_cloud import ToneAnalyzerV3
import csv
import pandas


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

PARSE_PRODUCTION_APLICATION_ID= "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB"
PARSE_PRODUCTION_REST_API_KEY = "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w"

PARSE_DEVELOPMENT_APLICATION_ID= "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB"
PARSE_DEVELOPMENT_REST_API_KEY = "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w"

if (PRODUCTION_ENVIRONMENT):

	{
  		Parse_Application_Id = PARSE_PRODUCTION_APLICATION_ID
  		Parse_REST_API_Key = PARSE_PRODUCTION_REST_API_KEY
	}
else:
	{
  		Parse_Application_Id = PARSE_DEVELOPMENT_APLICATION_ID
  		Parse_REST_API_Key = PARSE_DEVELOPMENT_REST_API_KEY
	}

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
	oldest = {}
	for i in range(0,len(result['results'])):
	    twitterURL.append(result['results'][i]['manualTwitterURL'])
	    leadid.append(result['results'][i]['objectId'])
	    userid.append(result['results'][i]['user']['objectId'])
	for i in range(0,len(twitterURL)):
		alltweets = []
    	huntweets = []
    	oldestid=json.load(open("lastTweetId_tone.txt"))
	    try:
	    	oldestid = oldest.get(twitterURL[i])
	    except IndexError:
	        oldestid = '0'

    	if oldestid == '0':
        	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True)
    	else:
	    	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True, since_id = oldestid)
    	#new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True)
    	status_count = len(new_tweets)
        max_id = new_tweets[status_count - 1].id - 1 
        oldest[twitterURL[i]] = tweet.id
    	alltweets.extend(new_tweets)
    	for tweet in alltweets:
        	huntweets.append(tweet.text.encode("utf-8"))
    	huntweets = json.dumps(huntweets)

    	k = tone_analyzer.tone(text=huntweets,sentences=False)
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
		       	"last_tweet_tone_id": max_id,
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
    json.dump(oldest,open("lastTweetId_tone.txt","w"))
		
	return ('Successfully added tone values to Insights!')

@app.route('/personality')
def personalitytweets():

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
    	huntweets = []
    	oldest = {}
    	oldestid=json.load(open("lastTweetId_pers.txt"))
	    try:
	    	oldestid = oldest.get(twitterURL[i])
	    except IndexError:
	        oldestid = '0'

    	if oldestid == '0':
        	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True)
    	else:
	    	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True, since_id = oldestid)

    	new_tweets = api.user_timeline(screen_name =twitterURL[i],count=100, exclude_replies= True)
    	status_count = len(new_tweets)
        max_id = new_tweets[status_count - 1].id - 1
        oldest[twitterURL[i]] = tweet.id
    	alltweets.extend(new_tweets)
    	for tweet in alltweets:
        	huntweets.append(tweet.text.encode("utf-8"))
    	huntweets = json.dumps(huntweets)

    	r = requests.post('https://gateway.watsonplatform.net/personality-insights/api/v2/profile',auth=('14b0fbeb-89b2-4a04-a442-c6a21af1eed4','ec2MeIUi6SOY'),headers={'content-type': 'text/plain','accept': 'text/csv'},data=json.dumps(huntweets))
    	pers_value = [[r.text.encode("utf-8")] for x in r]

    	with open('pers.csv', 'wb') as f:
    		writer = csv.writer(f)
    		writer.writerow(["personality"])
    		writer.writerows(pers_value)
    	pass

    	data_pers = pandas.read_csv('pers.csv')
    	k = data_pers.iloc[1].str.split(",")

		
    	connection = httplib.HTTPSConnection('parseapi.back4app.com', 443)
    	connection.connect()
    	connection.request('POST', '/classes/Personality', json.dumps({
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
		     	"last_tweet_pers_id": max_id,
		       	"personality_big5_openness":k[0][30],
	       		"personality_big5_openness_facet_adventurousness":k[0][31],
	       		"personality_big5_openness_facet_artistic_interests":k[0][32],
	       		"personality_big5_openness_facet_emotionality":k[0][33],
	       		"personality_big5_openness_facet_imagination":k[0][34],
	       		"personality_big5_openness_facet_intellect":k[0][35],
	       		"personality_big5_openness_facet_liberalism":k[0][36],
	       		"personality_big5_conscientiousness":k[0][9],
	       		"personality_big5_conscientiousness_facet_achievement_striving":k[0][10],
	       		"personality_big5_conscientiousness_facet_cautiousness":k[0][11],
	       		"personality_big5_conscientiousness_facet_dutifulness":k[0][12],
	       		"personality_big5_conscientiousness_facet_orderliness":k[0][13],
	       		"personality_big5_conscientiousness_facet_self_discipline":k[0][14],
	       		"personality_big5_conscientiousness_facet_self_efficacy":k[0][15],
	       		"personality_big5_extraversion":k[0][16],
	       		"personality_big5_extraversion_facet_activity_level":k[0][17],
	       		"personality_big5_extraversion_facet_assertiveness":k[0][18],
	       		"personality_big5_extraversion_facet_cheerfulness":k[0][19],
	       		"personality_big5_extraversion_facet_excitement_seeking":k[0][20],
	       		"personality_big5_extraversion_facet_friendliness":k[0][21],
	       		"personality_big5_extraversion_facet_gregariousness":k[0][22],
	       		"personality_big5_agreeableness":k[0][2],
	       		"personality_big5_agreeableness_facet_altruism":k[0][3],
	       		"personality_big5_agreeableness_facet_cooperation":k[0][4],
	       		"personality_big5_agreeableness_facet_modesty":k[0][5],
	       		"personality_big5_agreeableness_facet_morality":k[0][6],
	       		"personality_big5_agreeableness_facet_sympathy":k[0][7],
	       		"personality_big5_agreeableness_facet_trust":k[0][8],
	       		"personality_big5_neuroticism":k[0][23],
	       		"personality_big5_neuroticism_facet_anger":k[0][24],
	       		"personality_big5_neuroticism_facet_anxiety":k[0][25],
	       		"personality_big5_neuroticism_facet_depression":k[0][26],
	       		"personality_big5_neuroticism_facet_immoderation":k[0][27],
	       		"personality_big5_neuroticism_facet_self_consciousness":k[0][28],
	       		"personality_big5_neuroticism_facet_vulnerability":k[0][29],
	       		"needs":k[0][45],
	       		"needs_need_challenge":k[0][44],
	       		"needs_need_closeness":k[0][45],
	       		"needs_need_curiosity":k[0][46],
	       		"needs_need_excitement":k[0][47],
	       		"needs_need_harmony":k[0][48],
	       		"needs_need_ideal":k[0][39],
	       		"needs_need_liberty":k[0][38],
	       		"needs_need_love":k[0][40],
	       		"needs_need_practicality":k[0][41],
	       		"needs_need_self_expression":k[0][42],
	       		"needs_need_stability":k[0][43],
	       		"needs_need_structure":k[0][44],
	       		"values":k[0][53],
	       		"values_value_conservation":k[0][49],
	       		"values_value_openness_to_change":k[0][51],
	       		"values_value_hedonism":k[0][50],
	       		"values_value_self_enhancement":k[0][52],
	       		"values_value_self_transcendence":k[0][53],
		        }), {
		       	"X-Parse-Application-Id": "9LT6MCUSdT4mnzlNkG2pS8L51wvMWvugurQJnjwB",
			  	"X-Parse-REST-API-Key": "6gwEVURQBIkh9prcc3Bgy8tRiJTFYFbJJkQsB45w",
		        "Content-Type": "application/json"
		    })
		
	json.dump(oldest,open("lastTweetId_pers.txt","w"))
	return ("Personality Insights added to the Database!. Status code: %d" % (r.status_code))


port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    app.run()

