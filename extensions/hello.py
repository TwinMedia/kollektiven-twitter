# -*- coding: utf-8 -*-
import json
import requests
import urllib2
import os
import datetime

os.system("clear")

# API-KEYS
resrobot = ""
bitly = ""

# Grabs time
now = datetime.datetime.now()
# Stores time in variables
currentDay = now.day
currentHour = now.hour
currentMinute = now.minute
currentYearMonth = str(now.year) + "" + str(now.month)

#When mentioned
def process_mention(status, settings):
    print status.user.screen_name,':', status.text.encode('utf-8')
    newString = status.text.lower().replace("@kollektiven ", "")
    try:
            # Splits tweet with two destinations
            destination = newString.split(' - ')
            # Makes whitespace Url-encoded for the API
            fromDest = destination[0].replace(" ","%20")
            toDest = destination[1].replace(" ","%20")
            # Sets the API URL with right data
            fromUrl = urllib2.urlopen('https://api.trafiklab.se/samtrafiken/resrobot/FindLocation.json?apiVersion=2.1&from=' + fromDest + '&coordSys=WGS84&key=' + resrobot)
            # Loads from the URL above
            fromData = json.load(fromUrl)
            # Sets the second API URL to get the destinations ID
            toUrl = urllib2.urlopen('https://api.trafiklab.se/samtrafiken/resrobot/FindLocation.json?apiVersion=2.1&from=' + toDest + '&coordSys=WGS84&key=' + resrobot)
            # Loads the URL above
            toData = json.load(toUrl)
            # Grabs departure locations ID
            fromID = fromData['findlocationresult']['from']['location'][0]['locationid']
            # Grabs arrival locations ID
            toID = toData['findlocationresult']['from']['location'][0]['locationid']
            # Whole Trips URL
            tripUrl = "https://api.trafiklab.se/samtrafiken/resrobot/Search.json?apiVersion=2.1&coordSys=RT90&fromId=" + str(fromID) + "&toId=" + str(toID) + "&searchType=F&key=" + resrobot
            
            print tripUrl # For development purposes, should be commented out
            # Opens the Trip URL response
            trippy = urllib2.urlopen(tripUrl)
            trippyData = json.load(trippy)

            # A link where the user could se more travel alternatives
            long_url = "http://resrobot.se/pages/FindLocation.action?alwaysUseResRobot=false&searchData%2FsearchType=F&dummy=true&searchData%2Ffrom="+fromDest+"&searchData%2Fto="+toDest+"&searchData%2FroundTrip=false&searchData%2FalternativeStations=true&searchData%2FptAlternativeStations=false&searchData%2FoutDay="+currentDay+"&searchData%2FoutYearMonth="+currentYearMonth+"&searchData%2FoutDepartureTime=true&searchData%2FoutHour="+currentHour+"&searchData%2FoutMinute="+currentMinute+"&searchData%2FreturnDay="+currentDay+"&searchData%2FreturnYearMonth="+currentYearMonth+"&searchData%2FreturnDepartureTime=true&searchData%2FreturnHour="+currentHour+"&searchData%2FreturnMinute="+currentMinute+"&advancedMode=false&transportModes%2Fx2000=true&transportModes%2Ftrain=true&transportModes%2Fbus=true&transportModes%2Fboat=true&transportModes%2FexpressBus=true&transportModes%2Fair=true&transportModes%2Fcar=true&searchButton=++S%F6k++"
            
            print long_url # For development purposes, should be commented out

            # Makes our loooong long_url into a bit.ly link
            query_params = {'access_token': bitly, 'longUrl': long_url }  
            
            # Tries to query data
            try:
                tripType = trippyData['timetableresult']['ttitem'][0]['segment'][0]['segmentid']['mot']['#text']
                tripNumber = trippyData['timetableresult']['ttitem'][0]['segment'][0]['segmentid']['carrier']['number']
                fromName = trippyData['timetableresult']['ttitem'][0]['segment'][0]['departure']['location']['name']
                toName = trippyData['timetableresult']['ttitem'][0]['segment'][0]['arrival']['location']['name']
                fromTime = trippyData['timetableresult']['ttitem'][0]['segment'][0]['departure']['datetime']
                toTime = trippyData['timetableresult']['ttitem'][0]['segment'][0]['arrival']['datetime']

                # Bit.ly API-request
                endpoint = "https://api-ssl.bitly.com/v3/shorten"
                response = requests.get(endpoint, params= query_params)
                data = json.loads(response.content)
                # Our bit.ly link
                short_link = data['data']['url']
                # Summerizes the reply-tweet inside a string
                answer = tripType+" "+str(tripNumber)+": "+fromName+" ("+fromTime+") - "+destination[1].title()+" ("+toTime+")  " + short_link
                print answer # For development purposes, should be commented out
                return dict(response=answer) # Sends our response tweet
    	    except:
    		    return dict(response="Error") # Sends an error tweet to the questioner
    except:
	foo = "bar" # For development purposes, should be commented out
