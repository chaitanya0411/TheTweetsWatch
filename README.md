Given 2 location names this project finds the geolocated Tweets
falling within the requested bounding boxes by processing twitters
streaming data and plots the N locations from which maximum tweets
were recorded using REDIS cache. It also finds the N most tweeted
hashtags(Trending topics) in the given area. 

Sample run command : python test.py -f "San Francisco" -s "Seattle"
