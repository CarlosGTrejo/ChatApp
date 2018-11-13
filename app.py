from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
# from pyreadline import Readline
import sys, os

#===================[Configuration]====================

user_name = str(input("Username: "))
channel = 'main'

pnconf = PNConfiguration()
pnconf.publish_key = ''
pnconf.subscribe_key = ''
pnconf.uuid = user_name
pnconf.ssl = False
pn = PubNub(pnconf)

#====================[Functions]======================

def send_msg(user, msg):
    data = {'user': str(user),
            'message': str(msg)}
    pn.publish().channel(channel).message(data).sync()


def banner(obj):
    print('\n','=' * (len(obj)+10), sep='')
    print('   [ {} ]'.format(obj))
    print('=' * (len(obj)+10),'\n')


def alert(text):
    data = {'alert': '{}'.format(text)}
    pn.publish().channel(channel).message(data).sync()


def get_input():
    message = input('{}: '.format(user_name))

    if message.lower() in ['!quit', '!exit']: # Clear screen and unsubscribe when quitting
        print('Quitting...')
        alert('{} left the channel'.format(user_name))
        pn.unsubscribe().channels(channel).execute()
        sys.stdout.flush()
        os._exit(0)

    else:
        data = {'user': str(user_name),
                'message': message}
        pn.publish().channel(channel).message(data).sync()

#=====================[Callback]=========================

class CustomListener(SubscribeCallback):

    def message(self, pubnub, message):
        if 'alert' in message.message:
            banner(message.message['alert'])

        elif message.message['user'] != user_name:
            #Readline.get_line_buffer
            print('\r{usr}: {msg}'.format(usr=message.message['user'], msg=message.message['message']))
            #sys.stdout.write('{}: '.format(user_name) + Readline.get_line_buffer) # <- FIX THIS
            sys.stdout.flush()

msg_listener = CustomListener()
#=======================[Main]========================

pn.add_listener(msg_listener)
pn.subscribe().channels(channel).execute()

def main():
    while True:
        get_input()


if __name__ == "__main__":
    main()
