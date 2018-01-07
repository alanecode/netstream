# NetStream

Given a hypothetical network with a specific structure (defined
[below](#network-definition)), `netstream` will listen to the twitter public
stream for actions on the social network which are determined to constitute
*interactions* between members of our hypothesised model network.

The application I have in mind for this tool is to aggregate the retrieved data
to gain a view on the ways in which individuals can, through their varied
interests, connect up otherwise disparate sets of ideas. However, by gathering
data at the disaggregated tweet level, I hope to make it useful to other
projects as well.

## Network definition

A network is defined by:

1. A set of people (nodes) who can each be identified by a (possibly unit) set
   of strings
2. Interactions between people (edges), for a given definition of 'interaction'

Details of what constitutes an interaction are given
[below](#defining-an-interaction).

## Project structure

`netstream` uses the [`tweepy`](http://www.tweepy.org) library for accessing
the Twitter API, and a PostgreSQL database to store relevant detected tweets.
It is broken down into two modules: `trawl.py` and `netprocess.py`.

### `trawl.py`

`trawl.py` pulls potentially interesting data out of the public stream into the
local database. It errs on the side of caution when it comes to selecting which
tweets to keep insofar as it will store all tweets, favourites and likes coming
from network members. While many of these activities won't correspond to
interactions between network members as initially defined, they may, for
example, help indicate new individuals who may be interesting to add to the
network for  subsequent experiments. This behaviour is predicated on the
assumption that the number of individuals in the model network is small enough
that they dont,  between them, generate much more than 1,000 or so actions/ day.
If this proves to be unrealistic the 'generous' data storage behaviour may need
to be reviewed.

### `netprocess.py`

`netprocess.py` contains the logic for sifting through tweets captured by
`trawl.py` to identify network interactions. Based on its configuration, it
will identify and categorise interactions between nodes, posting its results to
derived database tables. The idea is that `trawl.py` and `netprocess.py` run
asynchronously in separate processes so that, at any time, another user (such
as a web server) could log into the database and retrieve up-to-date information
about network interactions.

## Evidence of network interactions

### Identifying an individual

A tweet is deemed as evidence relating to a specific individual (and will be
captured in the database by `trawl.py`) if one of the following conditions
holds:

- It was sent from a handle known to belong to an individual in the model
  network
- A known handle liked the tweet
- A known individual retweeted the tweet
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
of a manual process including exploratory data analysis.

### Defining an interaction

The following scenarios are considered evidence of an interaction between
individual $i$ and individual $j$:

- A single tweet contains evidence relating to both $i$ and $j$ (as defined
  [above](#identifying-an-individual)).
- $i$ mentions $j$ in a tweet
- $i$ replies to a tweet by $j$
- $i$ likes a tweet by $j$
- $i$ retweets a tweet by $j$

These rules will be implemented in `netprocess.py` to update the database with
information describing network interactions.

## Implementation details

### Tweet object

Tweet object should include methods for identifying whether it should be
retained, and being able to report on the rule(s) according to which it was
retained subsequently. It should also provide access to data such as status
etc.
