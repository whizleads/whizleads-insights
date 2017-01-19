import os
from flask import Flask, request, render_template, jsonify
import tweepy
import sys
import requests
import json,httplib,urllib
from google.cloud import language
from watson_developer_cloud import ToneAnalyzerV3


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
  thirtytweets = []
  new_tweets = api.user_timeline(screen_name =twitterURL[i],count=30, exclude_replies= True)
  alltweets.extend(new_tweets)
  for tweet in alltweets:
      thirtytweets.append(tweet.text.encode("utf-8"))
  thirtytweets = json.dumps(thirtytweets)

  k =tone_analyzer.tone(text=thirtytweets,sentences=False)
  emo_tone = k["document_tone"]["tone_categories"][0]["tones"]
  lan_tone = k["document_tone"]["tone_categories"][1]["tones"]
  soc_tone = k["document_tone"]["tone_categories"][2]["tones"]

  
  et_score.append(emo_tone[0]["score"])
  lt_score.append(lan_tone[0]["score"])
  st_score.append(soc_tone[0]["score"])
  print et_score
  print lt_score
  print st_score
    
    #print score

    
  print ("******************************************************************************************************")






	

