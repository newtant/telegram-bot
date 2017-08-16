import requests
import json
import config

URL = 'https://api.telegram.org/bot{}/'.format(config.token)
self_chat = config.self_chat

def getPublicIP():
    content = requests.get('http://ifconfig.co/json')
    content = json.loads(content.text)
    return content['ip']

def getUrl(url):
    # print("Getting {}.".format(url))
    return requests.get(url)

def getUpdates(offset=None):
    request = URL + 'getUpdates'
    if offset:
        request += '?offset={}'.format(int(offset)+1)
    updates = getUrl(request)
    # updates = updates.text.decode("utf-8")
    updates = json.loads(updates.text)
    # try:
    #     print(updates)
    # except UnicodeEncodeError:
    #     print("Unicode, can't parse.")

    messages = []

    if updates['result']:
        last_update = updates['result'][-1]['update_id']
        # print('{}: {}'.format(last_update, updates['result'][-1]['message']['text']))
        for result in updates['result']:
            try:
                messages.append(result['message']['text'])
            except:
                print("Unicode, can't parse.")
        saveLastUpdate(last_update)
    return messages

def parseMessages(messages):
    for message in messages:
        print("Received message: \"{}\"".format(message))

        if message.lower() == 'ip':
            sendMessage(getPublicIP(), self_chat)

        if message.lower() == 'test':
            sendMessage("I'm awake.", self_chat)

def readLastUpdate():
    with open('update_id.txt', 'r') as logFile:
        return logFile.readline()

def saveLastUpdate(id):
    with open('update_id.txt', 'w') as logFile:
        logFile.writelines(str(id))    
    print('Done updating, current Update ID is {}.'.format(id))

def sendMessage(message, chat):
    request = URL + 'sendMessage?chat_id={}&text={}'.format(chat, message)
    print(getUrl(request).status_code)

if __name__ == '__main__':
    update_id = readLastUpdate()
    print('Fetching new messages, last Update ID was {}.'.format(update_id))
    updates = getUpdates(update_id)
    parseMessages(updates)