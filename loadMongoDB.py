import json
from pymongo import MongoClient

# Start up MongoDB
# ====================
client = MongoClient() # assuming you have the MongoDB server running ...

# list the databases in this MongoDB instance
client.database_names()

# start over fresh
db    = client['HTA0']
posts = db.posts
db.posts.remove({}) # remove the documents
# client.drop_database('HTA') # delete the database

db    = client['HTA0']
posts = db.posts

# read in the tweets and store those you're interested in
# =======================================================
with open('../../data packages/HTA_reversegeo0-mine.json', 'r')\
     as tweet_file:
    for line in tweet_file:
        tweet = json.loads(line)
        posts.insert(tweet)

posts.find({})
