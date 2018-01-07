#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Save potentially interesting tweets and other actions to a database.

"""
import os
import sys

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import time
import json

def get_API_credentials():
    """
    Read in Twitter API credentials from environment variables assumaed to have
    been set previously.

    """
    try:
        auth = {'TWITTER_CONSUMER_KEY': os.environ['TWITTER_CONSUMER_KEY'],
                'TWITTER_CONSUMER_SECRET': os.environ['TWITTER_CONSUMER_SECRET'],
                'TWITTER_ACCESS_TOKEN_KEY': os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                'TWITTER_ACCESS_TOKEN_SECRET': os.environ['TWITTER_ACCESS_TOKEN_SECRET']
                }
    except KeyError as e:
        print 'Error: check Twitter API key credentials are correctly set as ' \
              'environment variables.\n'+str(e)

        sys.exit(0)

    return auth

class SimpleStreamListener(StreamListener):
    """
    A basic stream listener useful for testing purposes. Simply prints the
    status of each tweet matching a term in the filter array.

    """

    def on_status(self, status):
        print(status.text)

# set up stream listener which sends selected tweets to database.
# Based on the gist here https://gist.github.com/ctufts/e38e0588bf6d8f32e99d
class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
		# collect all desired data fields
        if 'text' in all_data:
          tweet         = all_data["text"]
          created_at    = all_data["created_at"]
          retweeted     = all_data["retweeted"]
          username      = all_data["user"]["screen_name"]
          user_tz       = all_data["user"]["time_zone"]
          user_location = all_data["user"]["location"]
          user_coordinates   = all_data["coordinates"]

	  # if coordinates are not present store blank value
	  # otherwise get the coordinates.coordinates value
          if user_coordinates is None:
            final_coordinates = user_coordinates
          else:
            final_coordinates = str(all_data["coordinates"]["coordinates"])

	  # inser values into the db
          cursor.execute("INSERT INTO tableName (created_at, username, tweet, coordinates, userTimeZone, userLocation, retweeted) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (created_at, username, tweet, final_coordinates, user_tz, user_location, retweeted))
          cnx.commit()

          print((username,tweet))

          return True
        else:
          return True

    def on_error(self, status):
        print(status)


cred = get_API_credentials()
auth = OAuthHandler(cred['TWITTER_CONSUMER_KEY'], cred['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(cred['TWITTER_ACCESS_TOKEN_KEY'], cred['TWITTER_ACCESS_TOKEN_SECRET'])

# create stream and filter on a searchterm
twitterStream = Stream(auth, listener=SimpleStreamListener())
twitterStream.filter(track=["python"],
  languages = ["en"], stall_warnings = True)
