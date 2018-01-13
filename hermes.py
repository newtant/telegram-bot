import requests
import json
import config

URL = 'https://api.telegram.org/bot{}/'.format(config.token)
self_chat = config.self_chat

#####################
####### TO-DO #######
#####################

# apparently requests has json decoding builtin via .json()
# still can't handle stickers/unicode whatsoever

#####################
### BOT FUNCTIONS ###
#####################

def getPublicIP():
    content = requests.get('http://ifconfig.co/json')
    content = json.loads(content.text)
    return content['ip']

######################
## HELPER FUNCTIONS ##
######################

def getUpdates(offset=None):
    request = URL + 'getUpdates'
    if offset:
        request += '?offset={}'.format(int(offset)+1)
    updates = getUrl(request)
    updates = json.loads(updates.text)
    return updates


def parseMessages(updates):
    messages = []
    new_update = updates['result'][-1]['update_id']
    # print("Last Update ID: {}".format(new_update))
    saveNewUpdate(new_update)
    for result in updates['result']:
        try:
            messages.append(result['message']['text'])
        except:
            print("Unicode, can't parse.")

    for message in messages:
        print("Received message: \"{}\"".format(message.lower()))
        if message.lower() == 'ip':
            sendMessage(getPublicIP(), self_chat)
        elif message.lower() == 'test':
            sendMessage("I'm awake.", self_chat)


def getUrl(url):
    # print("Getting {}.".format(url))
    return requests.get(url)


def saveNewUpdate(id):
    with open('update_id.txt', 'w') as logFile:
        logFile.writelines(str(id))    
    print('Done updating, current Update ID is {}.'.format(id))


def sendMessage(message, chat):
    # print("Sending...")
    request = URL + 'sendMessage?chat_id={}&text={}'.format(chat, message)
    print(getUrl(request).status_code)


if __name__ == '__main__':
    with open('update_id.txt', 'r') as logFile:
        last_update = logFile.readline()
    # print('Fetching new messages, last Update ID was {}.'.format(last_update))
    updates = getUpdates(last_update)
    parseMessages(updates)