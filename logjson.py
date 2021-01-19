import re
import json
import pprint
import tail

file_to_watch = 'testlog.txt'

pattern = re.compile( r"{.*}" )

def match_intent( l ):

    s = pattern.search(l)
    if s:
        j = json.loads(s.group())
        print("{},".format(json.dumps(j, indent=2, sort_keys=True)))
#        pprint.pprint(j)


with open( file_to_watch ) as f:
    lines = [line.rstrip() for line in f]
    for l in lines:
        match_intent( l.rstrip() )

#tl = tail.Tail(file_to_watch)
#tl.register_callback( match_intent )
#tl.follow()
