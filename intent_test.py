import re
import json
import tail

file_to_watch = 'testlog.txt'
request_file = 'commands.txt'
csv_file = 'results.csv'

pattern = re.compile( r"{.*}" )

def next_request():
    f = open( request_file, 'r' )
    for line in f:
        yield line.rstrip()
    
    close(f)
    return None

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
    global current_request
    if not 'incoming_text' in l:
        return

    s = pattern.search(l)
    if s:
        j = json.loads(s.group())
        txt = j['incoming_text']
        if len(txt):
            print('{}: {}'.format(j['incoming_text'], j['result_intent']))

            step = decision()
            succ = step[0]
            retry = step[1]

            log_entry = '{},"{}","{}","{}","{}"\n'.format(j['time'],succ,current_request, j['incoming_text'], j['result_intent'])
            csv.write( log_entry )

            if not retry:
                current_request = next( req_iterator )
                if current_request is None:
                    quit()
                print( 'Next: {}'.format( current_request ))
            else:
                print( 'Retry: {}'.format( current_request ))
            
        else:
            print( 'No incoming text, retry: {}'.format(current_request) )
    else:
        print( 'No JSON' )


req_iterator = next_request()
current_request = next(req_iterator)
csv = open( csv_file, 'w')

help()
print( "First request: {}".format( current_request ))

tl = tail.Tail(file_to_watch)
tl.register_callback( match_intent )
tl.follow()
