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
import argparse

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
    except Exception as e:
        print(e)



#################################### Main ##############################

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('URL', type=str, help='target URL')
    parser.add_argument('-c', '--cookies', default="", type=str, help="URL encoded cookie payload separated by semicolon \
        :some_cookie1 = URL encoded value1; some_cookie2 = URL encoded value2")

    #parse inputs
    args = parser.parse_args()

    targetURL = args.URL

    try:
        cookies = dict(item.split("=") for item in args.cookies.strip().split(";"))
    except:
        print("Cookie format is wrong OR you have not url encoded the values.")
    
    inTrigger = 10

    sendRequest(targetURL, cookies)


if __name__ == "__main__":
    main()
