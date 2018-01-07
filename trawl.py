#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Save potentially interesting tweets and other actions to a database.

"""
import os
import sys

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
        print "Error: check Twitter API key credentials are correctly set as " \
              "environment variables.\n"+str(e)

        sys.exit(0)

    return auth

auth = get_API_credentials()
