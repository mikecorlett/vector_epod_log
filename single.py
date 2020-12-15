def append_to( fname, l):
    f = open( fname,'a' ) 
    f.write( '\n' )
    f.write( l )
    f.close()



f = open('incoming.txt')

for l in f.readlines():
    key = input( 'Next:')
    print(key)
    print(l)
    append_to( 'testlog.txt', l)