# NetStream
Given a hypothetical network with a specific structure (defined below),
`netstream` will listen to the twitter public stream for actions on the social
network which are determined to constitute *interactions* between members of
our hypothesised model network.

The application I have in mind for this tool is to aggregate the retrieved data
to gain a view on the ways in which individuals can, through their varied
interests, connect up otherwise disparate sets of ideas. However, by gathering
data at the disaggregated tweet level, I hope to make it useful to other
projects as well.

`netstream` uses the [`tweepy`](http://www.tweepy.org) library for accessing
the Twitter API, and a PostgreSQL database to store relevant detected tweets.

## Identifying an individual
A tweet is deemed as evidence relating to a specific individual if one of the
following holds:
- It was sent from a handle known to belong to an individual in the network
- A known handle is mentioned in the tweet
- The tweet is in reply to a known handle
- The tweet contains one of a set of regular expressions identifying the
  individual (such as their surname). In some cases, such regular expressions
  will only match if an additional string defining some sort of context is
  also found in the tweet. For example, we might always match
  `"Prof. Smarty Pants" ` but only match `"Prof. Pants"` if we also match
  `"Hull"` (where Prof. Smarty Pants is known to be a lecturer).

All such tweets will be recorded in the database. It will be assumed that any
pruning of 'noisy' irrelevant tweets will be performed on the database as part
of a manual process.

## Defining an interaction
A tweet is deemed as evidence of an interaction between user $i$ and user $j$
if:
- Matches for evidence of $i$ and evidence of $j$ occur in the same tweet
- $i$ favourites a tweet by $j$
- $i$ retweets a tweet by $j$
