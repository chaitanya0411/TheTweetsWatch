#!/usr/bin/python

import twitter
import json
import geopy
from geopy.geocoders import Nominatim
import redis
import sys
import getopt

LOCALHOST = 'localhost'
REDIS_PORT = 6379
ENGLISH = 'en'
CONSUMER_KEY = '3C2POd9olCQ2eD866DvIAgNx7'
CONSUMER_SECRET = 'grscajjABDyNsnVtLqAYJgJ9NExxizezhYiMotBkj8C76A3gCU'
ACCESS_TOKEN_KEY = '1522191547-FfifUKbxagKGHfWtVsswKBTEkNQqJO7UCfApbFo'
ACCESS_TOKEN_SECRET = 'vuCQ2xGkcJuWRjaNa4CY0L3i861ldmqgq0T85ytv7mwYe'
INCREMENT_COUNTER = 1
NO_OF_LOCATIONS = 5
QUEUE = 'tweet_locations_prority_queue'

#initialize redis
def initialize_redis():
    r_conn = redis.StrictRedis(host = LOCALHOST, port = REDIS_PORT, db=0)
    return r_conn

#set locations so that only geolocated Tweets
#falling within the requested bounding boxes will be included
def get_coordinates(location1, location2):
    geolocator = Nominatim()
    location1 = geolocator.geocode(location1)
    location2 = geolocator.geocode(location2)

    #set co-ordinates
    coordinates =[str(location1.longitude), str(location1.latitude),
                  str(location2.longitude), str(location2.latitude)]
    return coordinates

def get_languages():
    languages = [ENGLISH]
    return languages


def process(location1, location2):
    #initialize api with access keys
    api = twitter.Api(
	      consumer_key = CONSUMER_KEY,
	      consumer_secret = CONSUMER_SECRET,
	      access_token_key = ACCESS_TOKEN_KEY,
	      access_token_secret = ACCESS_TOKEN_SECRET
	  )

    r_conn = initialize_redis()
    coordinates = get_coordinates(location1, location2)
    languages = get_languages()
    
    #find relvant things from stream and store it in redis
    for line in api.GetStreamFilter(locations = coordinates, languages = languages):
        if line is not None:
            print "Tweet : " + line["text"]
            if line["user"] is not None:
        	if line["user"]["name"] is not None:
	            print "User Name : " + line["user"]["name"]     
                if line["user"]["location"] is not None:
                    location = line["user"]["location"]
                    print "Location : " + location
                    r_conn.zincrby(QUEUE, location, float(INCREMENT_COUNTER))
                print r_conn.zrevrange(QUEUE, 0, NO_OF_LOCATIONS - 1)

def main(argv):
   location1 = ''
   location2 = ''
   try:
      opts, args = getopt.getopt(argv,"hf:s:",["f=","s="])
   except getopt.GetoptError:
      print 'test.py -f <location1> -s <location2>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -f <location1> -s <location2>'
         sys.exit()
      elif opt in ("-f", "--f"):
         location1 = arg
      elif opt in ("-s", "--s"):
         location2 = arg
   process(location1, location2)

if __name__ == "__main__":
   main(sys.argv[1:])
