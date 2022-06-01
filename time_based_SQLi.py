import requests
import sys

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

def sendRequest(URL):
    '''
    Sends reuquest to target URL with specified payload

    Payload is gonna be some conditional SQL statement 
    '''

    #GET

    res = requests.get(URL)

    try:
        res.raise_for_status()
        print(res.status_code)
    except Exception as e:
        print(e)



#################################### Main ##############################

def main():

    targetURL = "https://acef1f511ed4ed4ec070456500bd00d0.web-security-academy.net/filter?category=Corporate+gifts"
    inTrigger = 10

    sendRequest(targetURL)


if __name__ == "__main__":
    main()
