import os
from talkmoresms import Talkmore

crew = [
    '',
    '',
]

hosts = {
    'row1': '178.164.22.2',
    'row2': '178.164.22.34',
    'row3': '178.164.22.66',
    'row4': '178.164.22.98',
    'row5': '178.164.22.130',
    'row6': '178.164.22.162',
    'row7': '178.164.22.194',
    'row8': '178.164.22.226',
    'row9': '178.164.23.2',
    'row10': '178.164.23.34',
}

t = Talkmore('', '')

def send(message):
    t.login()
    t.send(crew, message)


for row, host in hosts.items():
    response = os.system('ping -c 1 ' + host)

    if response == 0:
        print('{} is up'.format(host))
    else:
        print('{} is down'.format(host))
        message = 'The switch: {} does not respons, It looks like {} is down, please go take a look.'.format(host, row)
        send(message)
