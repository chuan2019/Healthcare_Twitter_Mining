import json, sys, datetime

# a list of reverse geo-tagged files to process
file_list = ["../data packages/HTA_reversegeo2.json",\
             "../data packages/HTA_reversegeo3.json"]

# read from each file in the list
for tweet_file_name in file_list:
    line_number = 0
    with open(tweet_file_name, "r") as tweet_file:
        print "--Processing file %s" %tweet_file_name

        # go line-by-line through each file
        for line in tweet_file:
            line_number += 1

            # convert a single line into json or report an error
            try:
                tweet = json.loads(line)
            except Exception, e:
                print "error reading json from file %s at line %d"%\
                      (tweet_file_name, line_number)
                print e
                continue

            # pull out the fields of interest
            retweets  = tweet['retweet_count']
            user_name = tweet['user']['name']
            text      = tweet['text']

            ISO2_cc   = tweet['geo_reverse']['country_code']
            city      = tweet['geo_reverse']['city']
            county    = tweet['geo_reverse']['county']
            FIPS      = tweet['geo_reverse']['FIPS']
            state     = tweet['geo_reverse']['state']
            zipcode   = tweet['geo_reverse']['zipcode']

            orig_file = tweet['topsy']['short_file_name']

            timestamp = tweet['timestamp']
            date_str  = datetime.datetime.fromtimestamp(int(timestamp)).\
                        strftime('%a %b %d, %Y %H:%M:%S')

            # print repeatedly re-tweeted tweets that have a country code
            if retweets > 500 and ISO2_cc != "":
                print "\n\n%d (%s) %s"%(retweets, user_name, text)
                print "%s %s %s %s %s %s"%\
                      (city, county, FIPS, state, zipcode, ISO2_cc)
                print "%s %s"% (date_str, orig_file)
                sys.stdout.flush()
            if line_number >= 100:
                break

