import urllib2
import json

def makePostQuery(url, data):
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response

def makeGetQuery(url):
    response = urllib2.urlopen(url).read()
    return response


def executeCommand(command):
    pass
    #if command == ''

#runs constantly to manage API requests for data
def api_control_loop():
    #makeGetQuery('http://localhost:6340/run/a5da3bd1-35e3-4926-9857-d575fd3a40d3')

    #url = 'http://cms634fantasyrunningapp-fantasyrunning.rhcloud.com/dataRequest'
    url = 'http://localhost:6340/dataRequest'
    while True:
        response = makeGetQuery(url)
        print 'response: ',
        print response
        print type(response)
        response = json.loads(response)
        print 'response after conversion: ',
        print response
        print type(response)
        commands = response['commands']
        print commands
        if len(commands) > 0:
            for command in response['commands']:
                print command
                executeCommand(command)
            break


if __name__ == "__main__":
    api_control_loop()