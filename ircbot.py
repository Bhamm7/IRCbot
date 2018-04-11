import socket, string, re, time

################## CONFIGURATION DATA ###################
#########################################################

# Don't touch these two
SERVER = 'irc.twitch.tv'
PORT = 6667
# These two are your twitch channel name! (Defaults to lowercase)
NICKNAME = 'Trancefury'
USERNAME = 'Trancefury'
# oAuth token generated from connecting your twitch at https://twitchapps.com/tmi/
PASSWORD = 'oauth:5nnti14gcr18214zsq23wt7728e5h7'
# Channel name.
CHANNEL = 'electricalskateboard'
# How many seconds between your spams
INTERVAL = 5
PLUG_INTERVAL = 3
# Total seconds to spam for
HOST_DURATION = 60
# Spam command
COMMAND = '!hostme'
PLUG_COMMAND = 'zeegers mom has got it goin on\nzeegers mom has got it goin on\nzeegers cant you see ur just not the dude for me\nI know it may be wrong but im in love with zeegers mom'

#########################################################
#########################################################



IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Connect():
    print("Connecting to server " + SERVER + ", as user " + USERNAME + ", with password " + PASSWORD + "to channel " + CHANNEL + "\n")
    IRC.connect((SERVER, PORT))
    SendData("PASS " + PASSWORD)
    SendData("USER " + USERNAME)
    SendData("NICK " + NICKNAME)
    channel = '#' + CHANNEL
    SendData("JOIN %s" % channel)

def SendData(command):
    IRC.send(bytes(command + '\n', 'utf-8'))
    # IRC.send("PRVMSG #" + CHANNEL + ":" + command + "\n")

def SpamHost():
    print("Hosting lottery active, spamming command: " + COMMAND + "every " + str(INTERVAL) + "second(s) for total duration of " + str(HOST_DURATION))
    startTime = time.time()
    currentTime = startTime
    while ((currentTime - startTime) <= HOST_DURATION):
        SendData("PRIVMSG #" + CHANNEL + " :" + COMMAND)
        print('Sent command: ' + COMMAND)
        time.sleep(INTERVAL)
        SendData("PRIVMSG #" + CHANNEL + " :" + PLUG_COMMAND)
        print('Sent command: ' + PLUG_COMMAND)
        time.sleep(PLUG_INTERVAL)
        currentTime = time.time()
    print("Hosting period ended.\n")


### Main ###
Connect()

while (1):
    buffer = IRC.recv(2048)
    text = buffer.decode('utf8', "ignore")
    # if re.search("PING", text): #check if server have sent ping command
    # if text[0] == "PING":
    #     send_data("PONG %s" % text[1]) #answer with pong as per RFC 1459
    # if re.search("^:(trancefury|electricalskateboard)", text):
    #     print (text)

    pattern = r':' + re.escape(CHANNEL) + r".+(lottery started|lottery in progress)"
    if re.search(pattern, text):
        SpamHost()
    