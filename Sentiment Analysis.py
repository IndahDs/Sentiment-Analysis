#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import csv
from textblob import TextBlob
import time
import json


# In[2]:


api_key = "API_KEY"
api_secret_key = "API_SECRET_KEY"
access_token = "ACCESS_TOKEN"
access_token_secret = "ACCESS_TOKEN_SECRET"
class StdoutListener(StreamListener):
  def on_data(self,data):
      try:
          data = json.loads(data)
          tweet = data['text']
          print(tweet)
          with open('tweet.csv', 'a', encoding='utf-8') as f:
            saveFile = open('bundle.csv', 'a')
            f.write(tweets)
            f.write('\n')
            f.close()
          return True
      except BaseException as e:
          print('Failed',(e))

      def on_error(self,status):
          print(status)


# In[3]:


auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
search_key = ""


# In[8]:


hasilSearch = api.search(q="#pandemi",lang="id", count=100)


# In[9]:


Result = []

for tweet in hasilSearch:
    tweet_properties = {}
    tweet_properties["tanggal_tweet"] =tweet.created_at
    tweet_properties["pengguna"] = tweet.user.screen_name
    tweet_properties["isi_tweet"] = tweet.text
    tweet_clear = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet.text).split())
    
    analysis = TextBlob(tweet_clear)
    try:
        analysis = analysis.translate(to="en")
    except Exception as e:
        print(e)
        
    if analysis.sentiment.polarity > 0.0 : 
        tweet_properties ["sentiment"] = "positive"
    elif analysis.sentiment.polarity == 0.0:
        tweet_properties ["sentiment"] = "neutral"
    else:
        tweet_properties ["sentiment"] = "negative"
        
    print(tweet_properties)
    
    if tweet.retweet_count > 0:
        if tweet_properties not in Result:
            Result.append(tweet_properties)
    else:
        Result.append(tweet_properties)
        


# In[10]:


Result


# In[11]:


tweet_positive = [t for t in Result if t["sentiment"]=="positive"]
tweet_neutral = [t for t in Result if t["sentiment"]=="neutral"]
tweet_negative = [t for t in Result if t["sentiment"]=="negative"]


# In[12]:


print("Result Analysis")
print("positive: ", len(tweet_positive), "({}%)".format(100*len(tweet_positive)/len(Result)))
print("neutral: ", len(tweet_neutral), "({}%)".format(100*len(tweet_neutral)/len(Result)))
print("negative: ", len(tweet_negative), "({}%)".format(100*len(tweet_negative)/len(Result)))


# In[13]:


tweet_negative


# In[ ]:




