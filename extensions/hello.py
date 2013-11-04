# -*- coding: utf-8 -*-
import json
import urllib2
import os

os.system("clear")

# API-KEY
resrobot = "c3fbe29843a7aeea0bc75a6d7591fcb0"

def process_mention(status, settings):
    print status.user.screen_name,':', status.text.encode('utf-8')
    newString = status.text.lower().replace("@kollektiven ", "")
    try:
            destination = newString.split(' - ')
            fromDest = destination[0].replace(" ","%20")
            toDest = destination[1].replace(" ","%20")
            #print fromDest + "." + toDest
            fromUrl = urllib2.urlopen('https://api.trafiklab.se/samtrafiken/resrobot/FindLocation.json?apiVersion=2.1&from=' + fromDest + '&coordSys=WGS84&key=' + resrobot)
            fromData = json.load(fromUrl)
            toUrl = urllib2.urlopen('https://api.trafiklab.se/samtrafiken/resrobot/FindLocation.json?apiVersion=2.1&from=' + toDest + '&coordSys=WGS84&key=' + resrobot)
            toData = json.load(toUrl)
            fromID = fromData['findlocationresult']['from']['location'][0]['locationid']
            toID = toData['findlocationresult']['from']['location'][0]['locationid']
            #print str(fromID) + ' - ' + str(toID)
            tripUrl = "https://api.trafiklab.se/samtrafiken/resrobot/Search.json?apiVersion=2.1&coordSys=RT90&fromId=" + str(fromID) + "&toId=" + str(toID) + "&searchType=F&key=" + resrobot
            #print tripUrl
            trippy = urllib2.urlopen(tripUrl)
            trippyData = json.load(trippy)
	    try:
		    tripType = trippyData['timetableresult']['ttitem'][0]['segment'][0]['segmentid']['mot']['#text']
		    tripNumber = trippyData['timetableresult']['ttitem'][0]['segment'][0]['segmentid']['carrier']['number']
		    fromName = trippyData['timetableresult']['ttitem'][0]['segment'][0]['departure']['location']['name']
		    toName = trippyData['timetableresult']['ttitem'][0]['segment'][0]['arrival']['location']['name']
		    fromTime = trippyData['timetableresult']['ttitem'][0]['segment'][0]['departure']['datetime']
		    toTime = trippyData['timetableresult']['ttitem'][0]['segment'][0]['arrival']['datetime']
		    answer = tripType+" "+str(tripNumber)+": "+fromName+" ("+fromTime+") - "+destination[1].title()+" ("+toTime+")  http://resrobot.se/pages/FindLocation.action?alwaysUseResRobot=false&searchData%2FsearchType=F&dummy=true&searchData%2Ffrom="+fromName+"&searchData%2Fto="
		    return dict(response=answer)
	    except (KeyError):
		    tripType = trippyData['timetableresult']['ttitem'][0]['segment'][1]['segmentid']['mot']['#text']
		    tripNumber = trippyData['timetableresult']['ttitem'][0]['segment'][1]['segmentid']['carrier']['number']
		    fromName = trippyData['timetableresult']['ttitem'][0]['segment'][1]['departure']['location']['name']
		    toName = trippyData['timetableresult']['ttitem'][0]['segment'][1]['arrival']['location']['name']
		    fromTime = trippyData['timetableresult']['ttitem'][0]['segment'][1]['departure']['datetime']
		    toTime = trippyData['timetableresult']['ttitem'][0]['segment'][1]['arrival']['datetime']
		    answer = tripType+" "+str(tripNumber)+": "+fromName+" ("+fromTime+") - "+toName+" ("+toTime+")  http://resrobot.se/pages/FindLocation.action?alwaysUseResRobot=false&searchData%2FsearchType=F&dummy=true&searchData%2Ffrom="+fromName+"&searchData%2Fto="
		    return dict(response=answer)
    except:
	foo = "bar"
		


"""
except UnicodeEncodeError:
	    errorResponse = "yaman @jackbillstrom"
	    return dict(response=errorResponse)


    if status.text.lower() == ('@%s unfollow' % settings.username):
        return dict(unfollow=True, response=u'If you insist… unfollowing.')

def process_follow(status, settings):
    print status.source.screen_name, 'followed.'
    return dict(follow=True, dm='Followed you back!')


def process_dm(status, settings):
    print status.direct_message.sender_screen_name,':', status.direct_message.text.encode('utf-8')
    if status.direct_message.text.lower() == 'hello':
        return dict(dm='Hello, %s!' % status.direct_message.sender_screen_name)
    else:
        return None

def process_status(status, settings):
    print status.user.screen_name,':', status.text.encode('utf-8')
"""
