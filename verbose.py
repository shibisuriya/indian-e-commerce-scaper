from termcolor import colored
msgTypeColors = {
    'Note': 'yellow',
    'Danger': 'red',
    'Success': 'green'
}
def verbosePrint(verbose, message, messageType):
    if(verbose == True):
        print(colored(messageType + ":", msgTypeColors[messageType]), colored(message, 'yellow'))