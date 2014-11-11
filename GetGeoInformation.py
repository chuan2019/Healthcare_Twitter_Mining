import json, sys, datetime

# a list of reverse geo-tagged files to process
##file_list = ["../data packages/HTA_reversegeo.json", \
##             "../data packages/HTA_reversegeo2.json",\
##             "../data packages/HTA_reversegeo3.json"]

file_list = ["../data packages/HTA_reversegeo2.json"]

geo_county_freq  = {}
geo_FIPSc_freq   = {}
geo_city_freq    = {}
geo_state_freq   = {}
geo_zipcode_freq = {}
geo_ISO2cc_freq  = {}
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
            if(ISO2_cc not in geo_ISO2cc_freq.keys()):
                geo_ISO2cc_freq[ISO2_cc] = 1
            else:
                geo_ISO2cc_freq[ISO2_cc] += 1

            city      = tweet['geo_reverse']['city']
            if(city not in geo_city_freq.keys()):
                geo_city_freq[city] = 1
            else:
                geo_city_freq[city] += 1
            
            county    = tweet['geo_reverse']['county']
            if(county not in geo_county_freq.keys()):
                geo_county_freq[county] = 1
            else:
                geo_county_freq[county] += 1
                
            FIPS      = tweet['geo_reverse']['FIPS']
            if(FIPS not in geo_FIPSc_freq.keys()):
                geo_FIPSc_freq[FIPS] = 1
            else:
                geo_FIPSc_freq[FIPS] += 1
            
            state     = tweet['geo_reverse']['state']
            if(state not in geo_state_freq.keys()):
                geo_state_freq[state] = 1
            else:
                geo_state_freq[state] += 1
            
            zipcode   = tweet['geo_reverse']['zipcode']
            if(zipcode not in geo_zipcode_freq.keys()):
                geo_zipcode_freq[zipcode] = 1
            else:
                geo_zipcode_freq[zipcode] += 1

            orig_file = tweet['topsy']['short_file_name']

            timestamp = tweet['timestamp']
            date_str  = datetime.datetime.fromtimestamp(int(timestamp)).\
                        strftime('%a %b %d, %Y %H:%M:%S')

            # print repeatedly re-tweeted tweets that have a country code
            if retweets > 500 and ISO2_cc != "":
                print "\n\n%d (%s) %s"%(retweets, user_name, text)
                print "\n%s %s %s %s %s %s"%\
                      (city, county, FIPS, state, zipcode, ISO2_cc)
                print "\n%s %s"% (date_str, orig_file)
                sys.stdout.flush()
                
