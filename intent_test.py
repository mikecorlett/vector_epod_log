import re
import json
import tail

file_to_watch = 'testlog.txt'
cmd_file = 'commands.json'
csv_file = 'results.csv'

current_cmd = None

pattern = re.compile( r"{.*}" )

def help():
    print("Commands")
    print("h - help")
    print("m - match and continue")
    print("r - match and repeat")
    print("f - fail and continue")
    print("s - fail and repeat")

# prompt user, returns tuple (a,b)
# a - Y|N for success / fail
# b - true to retry, false to step to next command
def decision():
    resultmap = { 
        'm' : ('Y',False),
        'r' : ('Y',True),
        'f' : ('N',False),
        's' : ('N',True)
    }

    while True:
        key = input('?:')

        if not len(key):
            continue

        r = resultmap.get(key[0])
        if r is not None:
            return r
        else:
            continue


def match_intent( l ):
    global current_cmd
    if not 'incoming_text' in l:
        return

    s = pattern.search(l)
    if s:
        j = json.loads(s.group())
        txt = j['incoming_text']
        if len(txt):
            print('{}: {}'.format(j['incoming_text'], j['result_intent']))

            if current_cmd['intent'] == j['result_intent']:
                print( "Good match" )
                succ = "Y"
                retry = False
            else:
                step = decision()
                succ = step[0]
                retry = step[1]

            log_entry = '{},"{}","{}","{}","{}"\n'.format(j['time'],succ,current_cmd['request'], j['incoming_text'], j['result_intent'])
            csv.write( log_entry )

            if not retry:
                current_cmd = next( cmd_iterator )
                if current_cmd is None:
                    quit()
                intent_prompt(current_cmd)
            else:
                print( 'Retry: {}'.format( current_cmd['request'] ))
        else:
            print( 'No text, retry: {}'.format(current_cmd['request']) )
    else:
        print( 'No JSON' )


def load_intents( intentfile ):
    f = open(intentfile, 'r') 
    idict = json.load(f)
    return idict


def intent_prompt( i ):
    print( 'Intent:{} "{}"'.format(i['intent'], i['request']))

cmd_list = load_intents(cmd_file)
cmd_iterator = iter(cmd_list)

current_cmd = next(cmd_iterator)
csv = open( csv_file, 'w')

help()
intent_prompt(current_cmd)

tl = tail.Tail(file_to_watch)
tl.register_callback( match_intent )
tl.follow()
